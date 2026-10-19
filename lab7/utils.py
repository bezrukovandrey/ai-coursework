import numpy as np
import torch
import matplotlib.pyplot as plt

def rolling_window(series, window_size, stride):
    return np.array([series[i : (i + window_size)] for i in range(0, series.shape[0] - window_size + 1, stride)])

def to_timeseries_input(series, lookback, lookahead, stride=1):
    inputs = rolling_window(series[:-lookahead], lookback, stride)
    outputs = rolling_window(series[lookback:], lookahead, stride)
    return inputs, outputs


def splitDate(dates,cutoff):
    train_date = [x for x in dates if x <= cutoff]
    test_date = sorted(list(set(dates) - set(train_date)))
    return train_date, test_date


class Trainer:
    def __init__(self, model, train_loader, val_loader, test_loader, criterion, optimizer, device):
        """
        A utility class for training, validating and testing a PyTorch model.

        Attributes:
            model (nn.Module): The PyTorch model to train.
            train_loader (DataLoader): The DataLoader for the training data.
            val_loader (DataLoader): The DataLoader for the validation data.
            test_loader (DataLoader): The DataLoader for the test data.
            criterion (nn.Module): The loss function.
            optimizer (Optimizer): The optimizer.
            device (torch.device): The device to train on (e.g., 'cpu' or 'cuda').

        Methods:
            train(epochs, patience): Trains the model for a given number of epochs, with early stopping.
            evaluate(): Evaluates the model on the test data.
            predict(inputs): Makes predictions on a batch of inputs.
            plot_metrics(train_loss, val_loss, train_acc, val_acc): Plots training and validation loss and accuracy over time.
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.model.to(device)
        
    def train(self, epochs, patience=3):
        train_losses = []
        train_maes = []
        val_losses = []
        val_maes = []
        patience_counter = 0
        maes_max = 5e10
        for epoch in range(epochs):
            # Training
            self.model.train()
            running_loss = 0.0
            running_mae = 0.0
            for inputs, labels in self.train_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                mae = torch.abs(outputs - labels).mean()
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item() * inputs.size(0)
                running_mae += mae.item() * inputs.size(0)
            epoch_loss = running_loss / len(self.train_loader.dataset)
            epoch_mae = running_mae / len(self.train_loader.dataset)
            train_losses.append(epoch_loss)
            train_maes.append(epoch_mae)
            
            # Validation
            self.model.eval()
            running_val_loss = 0.0
            running_val_mae = 0.0
            with torch.no_grad():
                for inputs, labels in self.val_loader:
                    inputs, labels = inputs.to(self.device), labels.to(self.device)
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, labels)
                    mae = torch.abs(outputs - labels).mean()
                    running_val_loss += loss.item() * inputs.size(0)
                    running_val_mae += mae.item() * inputs.size(0)
            epoch_val_loss = running_val_loss / len(self.val_loader.dataset)
            epoch_val_mae = running_val_mae / len(self.val_loader.dataset)
            val_losses.append(epoch_val_loss)
            val_maes.append(epoch_val_mae)
            print(f"Epoch {epoch} | Train Loss: {epoch_loss:.4f} | Train MAE: {epoch_mae:.4f} | Val Loss: {epoch_val_loss:.4f} | Val MAE: {epoch_val_mae:.4f}")
            # Early stopping
            if epoch_val_mae < maes_max:
                maes_max = epoch_val_mae
                patience_counter = 0
            else:
                patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping due to no improvement after {} epochs".format(patience))
                break
        return train_losses, train_maes, val_losses, val_maes
    
    def evaluate(self):
        self.model.eval()
        total_mae = 0.0
        total_samples = 0
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                mae = torch.abs(outputs - labels).mean()
                total_mae += mae.item() * inputs.size(0)
                total_samples += inputs.size(0)
        test_mae = total_mae / total_samples
        print(f'Test MAE: {test_mae:.4f}')
        return test_mae
    
    def predict(self, inputs):
        self.model.eval()
        with torch.no_grad():
            inputs = inputs.to(self.device)
            outputs = self.model(inputs)
            _, preds = torch.max(outputs, 1)
        return preds
    
    @staticmethod
    def plot_metrics(train_loss, val_loss, train_metric, val_metric):
        epochs = range(1, len(train_loss) + 1)

        fig, axs = plt.subplots(2)

        # Subplot for loss
        axs[0].plot(epochs, train_loss, 'g', label='Training Loss')
        axs[0].plot(epochs, val_loss, 'b', label='Validation Loss')
        axs[0].set_title('Training and Validation Loss')
        axs[0].set_xlabel('Epochs')
        axs[0].set_ylabel('Loss')
        axs[0].legend()

        # Subplot for accuracy
        axs[1].plot(epochs, train_metric, 'g', label='Training MAE')
        axs[1].plot(epochs, val_metric, 'b', label='Validation MAE')
        axs[1].set_title('Training and Validation MAE')
        axs[1].set_xlabel('Epochs')
        axs[1].set_ylabel('MAE')
        axs[1].legend()

        plt.tight_layout()
        plt.show()
    
    
def PredictReconstruction(model, dataloader, lookahead, device):
    prediction = []
    target = []
    model.eval()
    with torch.no_grad():
        for x,y in dataloader:
            x = x.to(device)
            y = y.to(device)
            out = model(x)
            prediction.append(out)
            target.append(y)
    prediction = torch.cat(prediction, dim=0)
    target = torch.cat(target, dim=0)
    flatten_target = target.view(-1,lookahead)[::lookahead].flatten()
    flatten_pred = prediction.view(-1,lookahead)[::lookahead].flatten()
    return flatten_target.cpu().numpy(), flatten_pred.cpu().numpy()


def PlotResult(target, pred):
    plt.figure(figsize=(10,5))
    plt.plot(target, label="target")
    plt.plot(pred, label="prediction")
    plt.legend()
    plt.show()