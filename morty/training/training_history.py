import matplotlib.pyplot as plt
import pandas as pd

'''

'''

def build_table(headers, rows, digits=4):
    """
    Build a text table from headers and rows.

    Output example:
                    Train   Validation 

        loss        0.0228    0.0137
        accuracy    0.9933    0.9969
    """
    header_item_lens = [len(item) for item in headers]

    width = max(*header_item_lens, digits)

    head_fmt = '{:>{width}s}' + ' {:>9} ' * len(headers)
    row_fmt = ' {:>9}' + ' {:>9.{digits}f}' * 2 + '\n' 

    table = head_fmt.format('', *headers, width=width)
    table += '\n\n'

    for row in rows:
        table += row_fmt.format(*row, width=width, digits=digits)
    
    return table


def plot_training_history(
    training_history, 
    metrics=['loss', 'accuracy'], 
    best_epoch_metric='val_accuracy', 
    figsize=(15, 5)
):
    """
    Plot Keras training history comparing metrics on train and validation datasets
    """
    training_history_df = pd.DataFrame(training_history.history)

    best_epoch = np.argmax(training_history_df[best_epoch_metric])

    _, axes = plt.subplots(1, len(metrics), figsize=figsize)

    for idx, metric in enumerate(metrics):
        training_history_df[[metric, 'val_' + metric]].plot(
            title=metric, 
            grid=True, 
            ax=axes[idx]
        )
        plt.gca().set_ylim(0, 1)
        
        axes[idx].axvline(
            best_epoch,
            ls='--',
            c='k',
            lw=1,
        )
    
    rows = []
    
    for metric in metrics:
        rows.append([
            metric, 
            training_history_df[metric][best_epoch], 
            training_history_df['val_' + metric][best_epoch]]
        )
    
    return build_table(['Train', 'Validation'], rows)
