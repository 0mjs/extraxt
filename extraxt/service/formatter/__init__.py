class FormatService:
    def __init__(self, fields):
        self.fields = fields

    def format(self, content):
        data = {}
        for section, keys in self.fields.items():
            data[section] = {key: content.get(key, None) for key in keys}
        return data

    def apply(self, data, output, filter=None):
        for category, keys in self.fields.items():
            for key in keys:
                if key in data.get(category, {}):
                    item = data[category][key]
                    if isinstance(item, str):
                        item_key = item.strip()
                        value = self.basic(item_key)
                    else:
                        value = self.basic(item)
                    if value != filter:
                        output[category.lower()][key] = value
                        self.medication(key, value, output)

    def basic(self, value):
        return {"No": False, "Yes": True, "Unknown": "unknown", "": None}.get(
            value, value
        )

    def medication(self, key, value, output):
        if value is None or not isinstance(value, str):
            return
        if key == "anticoagulant_use":
            parts = value.split(" ", 1)
            if len(parts) == 2 and parts[0] in ["No", "Yes"]:
                output["medication"]["anticoagulant_use"] = parts[0]
                output["medication"]["current_medication"] = parts[1]
