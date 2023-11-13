import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, seq_length, output_dim, num_layers):
        super(LSTM, self).__init__()
        self.num_layers = num_layers
        self.seq_length = seq_length
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim, bias=True)

    def forward(self, x):
        x, _status = self.lstm(x)
        x = self.fc(x[:, -1])
        return x
    
    def reset_hidden(self):
        self.hidden = (
            torch.zeros(self.num_layers, self.seq_length, self.hidden_dim),
            torch.zeros(self.num_layers, self.seq_length, self.hidden_dim)
        )


def build_dataset(time_series, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(time_series)-seq_length):
        _x = time_series[i:i+seq_length, :]
        _y = time_series[i+seq_length, [-1]]
        dataX.append(_x)
        dataY.append(_y)

    return np.array(dataX), np.array(dataY)

def MAE(y, y_pred):
    return np.mean(np.abs(y - y_pred))


def train_model(**kwargs):

    # Read CSV file and first column as index
    df = pd.read_csv('/opt/airflow/data/stockdata.csv', index_col=0)

    # Params
    seq_length = 10
    batch = 100
    train_percentage = 0.7 # Train=70%, Test=30%

    # Train-test split
    train_size = int(len(df)*train_percentage)
    train_set = df[0:train_size]  
    test_set = df[train_size-seq_length:]

    # Scaling
    scaler_x = MinMaxScaler()
    scaler_x.fit(train_set.iloc[:, :-1])

    train_set.iloc[:, :-1] = scaler_x.transform(train_set.iloc[:, :-1])
    test_set.iloc[:, :-1] = scaler_x.transform(test_set.iloc[:, :-1])

    scaler_y = MinMaxScaler()
    scaler_y.fit(train_set.iloc[:, [-1]])

    train_set.iloc[:, -1] = scaler_y.transform(train_set.iloc[:, [-1]])
    test_set.iloc[:, -1] = scaler_y.transform(test_set.iloc[:, [-1]])

    trainX, trainY = build_dataset(np.array(train_set), seq_length)
    testX, testY = build_dataset(np.array(test_set), seq_length)


    trainX_tensor = torch.FloatTensor(trainX)
    trainY_tensor = torch.FloatTensor(trainY)

    testX_tensor = torch.FloatTensor(testX)
    testY_tensor = torch.FloatTensor(testY)


    dataset = TensorDataset(trainX_tensor, trainY_tensor)

    dataloader = DataLoader(dataset,
                            batch_size=batch,
                            shuffle=True,  
                            drop_last=True)

    ## Train

    # Hyperparameters
    input_dim = 5
    hidden_dim = 10
    output_dim = 1
    num_layers = 1
    learning_rate = 0.01
    num_epochs = 100

    # Initialize the model
    model = LSTM(input_dim, hidden_dim,seq_length,output_dim, num_layers)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in dataloader:
            x, y = batch
            model.reset_hidden()
            outputs = model(x)
            loss = criterion(outputs, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_loss = total_loss / len(dataloader)
        print(f'Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.4f}')

    ## Test

    # Evaluate the model on the test set
    model.eval()
    predictions = []
    total_loss = 0

    with torch.no_grad():
        for i in range(len(testX_tensor)):
            model.reset_hidden()
            pred = model(torch.unsqueeze(testX_tensor[i], 0))
            pred = torch.flatten(pred).item()
            predictions.append(pred)

        # Inverse transform
        pred_inverse = scaler_y.inverse_transform(np.array(predictions).reshape(-1, 1))
        testY_inverse = scaler_y.inverse_transform(testY)

    print(f'MAE: {MAE(testY_inverse, pred_inverse):.4f}')

    # Save the model with date
    # Today's date as yyyy-mm--dd
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    torch.save(model, f'/opt/airflow/data/model/model_{today}.pt')

    # parse index of test_set
    test_set_index = test_set.index

    # Plot the results
    plt.figure(figsize=(20, 10))
    plt.title(f"2021-05-14 ~ {today} KOSPI Predictions vs Actual")
    plt.plot(test_set_index[20:], testY_inverse[10:], label='Actual')
    plt.plot(test_set_index[20:], pred_inverse[10:], label='Predicted')

    ## Set x-axis as dates
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.legend()

    # Save the plot
    plt.savefig(f'/opt/airflow/data/plot/plot_{today}.png')

    return MAE(testY_inverse, pred_inverse)