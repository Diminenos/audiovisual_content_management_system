import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from collections import defaultdict
from sklearn.metrics import classification_report

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# AudioCNN Model
class AudioCNN(nn.Module):
    def __init__(self, num_classes):
        super(AudioCNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),

            nn.Conv2d(16, 32, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),

            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 10))  # Prevents zero-size error
        )

        self.flattened_size = 64 * 1 * 10
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(self.flattened_size, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

# Custom Dataset
class CustomDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        features = self.features[index].unsqueeze(0)  # Add a channel dimension
        labels = self.labels[index]
        return features, labels

# Save Best Model
class SaveBestModel:
    def __init__(self, best_valid_loss=float('inf')):
        self.best_valid_loss = best_valid_loss

    def __call__(self, current_valid_loss, fold, epoch, model):
        if current_valid_loss < self.best_valid_loss:
            self.best_valid_loss = current_valid_loss
            print(f"\nSaving best model for Fold {fold+1}, Epoch {epoch+1}")
            torch.save(model.state_dict(), f'best_model_fold_{fold+1}.pth')

# Evaluate Model
def evaluate_model(model, dataloader, device):
    model.eval()
    y_true, y_pred = [], []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)

    return accuracy, precision, recall, f1

# Load Data
loaded_data = torch.load("C:/Users/User/Desktop/create algorithm/spectrogram_dataset.pt")
loaded_features = loaded_data["features"]
loaded_labels = loaded_data["labels"]

# Initialize Stratified K-Fold
num_folds = 3
skf = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=42)

# Hyperparameters
EPOCHS = 30
batch_size = 32
num_classes = 3


# Initialize metrics storage
metrics_per_fold = defaultdict(list)

# Stratified K-Fold Cross-Validation
for fold, (train_idx, test_idx) in enumerate(skf.split(loaded_features, loaded_labels)):
    print(f"\n{'='*30}\nStarting Fold {fold+1}/{num_folds}\n{'='*30}")

    # Split dataset into train and test
    train_features, test_features = loaded_features[train_idx], loaded_features[test_idx]
    train_labels, test_labels = loaded_labels[train_idx], loaded_labels[test_idx]

    # Create validation set from the training data (10% of training data)
    train_features, val_features, train_labels, val_labels = train_test_split(
        train_features, train_labels, test_size=0.1, stratify=train_labels, random_state=42
    )

    # Create Datasets and DataLoaders
    train_dataset = CustomDataset(train_features, train_labels)
    val_dataset = CustomDataset(val_features, val_labels)
    test_dataset = CustomDataset(test_features, test_labels)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # Initialize model, optimizer, and loss
    model = AudioCNN(num_classes).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()
    save_best_model = SaveBestModel()

    # Training Loop
    for epoch in range(EPOCHS):
        model.train()
        train_loss, train_acc = 0, 0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)

            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            train_acc += (outputs.argmax(1) == y_batch).sum().item()

        train_loss /= len(train_loader)
        train_acc /= len(train_dataset)

        # Validation Loop
        val_loss, val_acc = 0, 0
        model.eval()
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)

                val_loss += loss.item()
                val_acc += (outputs.argmax(1) == y_batch).sum().item()

        val_loss /= len(val_loader)
        val_acc /= len(val_dataset)

        print(f"Epoch {epoch+1:03}: | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

        # Save the best model for this fold
        save_best_model(val_loss, fold, epoch, model)

    # Evaluate the model on the test set
    test_accuracy, test_precision, test_recall, test_f1 = evaluate_model(model, test_loader, device)
    metrics_per_fold['accuracy'].append(test_accuracy)
    metrics_per_fold['precision'].append(test_precision)
    metrics_per_fold['recall'].append(test_recall)
    metrics_per_fold['f1_score'].append(test_f1)

    print(f"\nFold {fold+1} Results: Accuracy: {test_accuracy:.4f}, Precision: {test_precision:.4f}, Recall: {test_recall:.4f}, F1-Score: {test_f1:.4f}")

    if fold == num_folds - 1:  # Only for the last fold
        y_true, y_pred = [], []

        model.eval()
        with torch.no_grad():
            for X_batch, y_batch in test_loader:
                X_batch = X_batch.to(device)
                outputs = model(X_batch)
                y_pred.extend(outputs.argmax(1).cpu().numpy())  
                y_true.extend(y_batch.cpu().numpy())  

        
        print("\nClassification Report for Last Fold:")
        print(classification_report(y_true, y_pred, digits=4))

# Summary of all folds
print("\nCross-Validation Results:")
for metric, values in metrics_per_fold.items():
    print(f"{metric.capitalize()}: {sum(values)/num_folds:.4f} ± {torch.std(torch.tensor(values)):.4f}")