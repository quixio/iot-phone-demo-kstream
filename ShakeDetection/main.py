
#from quix_function import QuixFunction
import os
from setup_logger import logger
from queue import Queue
from threading import Thread
from quix_function import QuixFunction
from queue_helper import consume_queue, stop
from bigquery_helper import connect_bigquery, create_paramdata_table, create_metadata_table, create_eventdata_table, create_properties_table, create_parents_table

from streamingdataframes import Application
from streamingdataframes.models.rows import Row
from streamingdataframes.models.serializers import (
    QuixTimeseriesSerializer,
    QuixDeserializer,
    JSONDeserializer
)

# Quix app has an option to auto create topics
# Quix app does not require the broker being defined
app = Application.Quix("big-query-sink-v3", auto_offset_reset="earliest")
input_topic = app.topic(os.environ["input"], value_deserializer=QuixDeserializer())



def print_row(row: Row):
    print(row)

# Hook up to termination signal (for docker image) and CTRL-C
logger.info("Listening to streams. Press CTRL-C to exit.")

def before_shutdown():
    stop()

# "Gold" members get realtime notifications about purchase events larger than $1000
sdf = app.dataframe(topics_in=[input_topic])
sdf = sdf.apply(print_row)  # easy way to print out


app.run(sdf)