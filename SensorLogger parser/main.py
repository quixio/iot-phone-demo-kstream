import os
from quixstreams import Application, State
from quixstreams.models.serializers.quix import QuixDeserializer, QuixTimeseriesSerializer
import json

app = Application.Quix("transformation-v5", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=QuixDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=QuixTimeseriesSerializer())

sdf = app.dataframe(input_topic)

def expand_values(row: dict):
    row.update(row["values"])

    del row["values"]

    return row

# Here put transformation logic.
sdf = sdf.update(lambda value: print(value))
sdf = sdf.apply(lambda value: json.loads(value["Value"])["payload"], expand=True)
sdf = sdf.apply(expand_values)
sdf["Timestamp"] = sdf["time"]
#sdf = sdf.update(lambda row: print(row))

#sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)