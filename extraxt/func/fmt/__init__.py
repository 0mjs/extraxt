class Formatter:
    def __init__(self, fields):
        self.fields = fields
        print(f"Extraxt: Initialized Formatter service with fields {fields.keys()}...")

    def format(self, content):
        data = {}
        for section, keys in self.fields.items():
            data[section] = {key: content.get(key, None) for key in keys}
        return data

    def apply(self, data, output, filter=None):
        print(f"Extraxt Formatter: Applying basic formatting to data...")
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

    def basic(self, value):
        return {"No": False, "Yes": True, "Unknown": "unknown", "": None}.get(
            value, value
        )
