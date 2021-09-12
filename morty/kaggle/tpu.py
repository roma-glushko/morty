import tensorflow as tf


# Kaggle TPU related utils

def enable_tf_tpu_support() -> tf.distribute.Strategy:
    """
    Enable TPU support on Kaggle environment
    """
    try:
        tpu_cluster = tf.distribute.cluster_resolver.TPUClusterResolver()
        print(f"Device: {tpu_cluster.master()}")

        tf.config.experimental_connect_to_cluster(tpu_cluster)
        tf.tpu.experimental.initialize_tpu_system(tpu_cluster)
        tpu_strategy = tf.distribute.experimental.TPUStrategy(tpu_cluster)
    except:  # noqa
        tpu_strategy = tf.distribute.get_strategy()

    print(f"Number of replicas: {tpu_strategy.num_replicas_in_sync}")

    return tpu_strategy
