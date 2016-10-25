from subfind_web.bootstrap import container


class ConfigService(object):
    def __init__(self):
        self.config = container.get('Config')
        self.validator_manager = container.get('ValidatorManager')
        self.data_provider = container.get('DataProvider')

    def index(self):
        return self.config.to_json()

    def update(self, **kwargs):
        update = {}
        config = container.get('Config')

        for field_name in ['src', 'lang', 'providers']:
            push_value = kwargs.get('%s-$push' % field_name)
            if push_value:
                push_value = self.validator_manager.validate_field(field_name, push_value)

                tmp = set(config[field_name])
                tmp.add(push_value)
                update[field_name] = sorted(list(tmp))

            remove_value = kwargs.get('%s-$remove' % field_name)
            if remove_value:
                remove_value = self.validator_manager.validate_field(field_name, remove_value)

                tmp = set(config[field_name])
                if remove_value in tmp:
                    tmp.remove(remove_value)
                    update[field_name] = sorted(list(tmp))

        for bool_field in ['force', 'remove']:
            bool_value = kwargs.get(bool_field)
            if bool_value is None:
                continue

            if bool_value == 'true':
                bool_value = True
            else:
                bool_value = False

            update[bool_field] = bool_value

        for int_field in ['min-movie-size', 'max-sub']:
            int_value = kwargs.get(int_field)
            if int_value is None:
                continue

            try:
                int_value = int(int_value)
            except ValueError:
                continue

            update[int_field] = int_value

        config.update(update)

        config.save()

        if 'src' in update:
            self.data_provider.build_data()

        return config.to_json()
