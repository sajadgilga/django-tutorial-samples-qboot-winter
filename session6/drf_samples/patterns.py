class SampleBorg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


a = SampleBorg()
b = SampleBorg()
c = SampleBorg()

a.x = "something"

print(a.x)
print(b.x)
print(c.x)


class Controller:
    def handle(self):
        # logic
        repo = Repository()
        result = repo.get_users()
        print(result)
        # logic


class Repository:
    def get_users(self):
        ds = PsqlDatasource()
        api_ds = ApiDatasource()
        api_result = api_ds.call_api({"name": "x"})
        db_result = ds.filter({'name': 'x'})
        return api_result + db_result

    def edit_documents(self, **kwargs):
        ds = ApiDatasource()
        ds.call_api({"extra": "something"})


class PsqlDatasource:
    def __init__(self):
        self.connect()

    def connect(self):
        pass

    def filter(self, **kwargs):
        pass

    def get(self):
        pass

    def edit(self):
        pass


class ApiDatasource:
    def __init__(self):
        pass

    def login(self):
        pass

    def call_api(self):
        pass
