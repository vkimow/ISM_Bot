class SpreadsheetIds:
    info = '1T36DM8mLYkgg7-vYCpEtD_FIP7CKdf61r45UkUE49BI'
    services = '1MvD4D6v3Bz6MD4gRSz8QbjW6w6ElWNduCc7vjUqEAdQ'
    users = '1b_WZy7rQbnfQvvE-j3V6JObkO7d1jC1KA7twlng0xrI'
    admins = '1HHChEXLzpXLGgx70HPhLaaGwP2EGVXHjPvXbKaGntQo'
    education = '1PodZjrLIGyE1hCPHGzmc09KSPiDbPSBIb52w0w96Ul8'


class BotTokens:
    main = '5600845189:AAHnJX5AZl3mKz7V6agQndnVyvYFq6cfjNM'
    test = '5428034932:AAGBjzKvAiM8dZ205GEOY9yM1wWu2FZrfYo'

class Paths:
    resource = 'resource'
    local = resource + '/local'
    remote = resource + '/remote'
    data = local + '/data'
    actions = remote + '/actions'
    backgrounds = remote + '/backgrounds'
    specialists = remote + '/specialists'

class Resources:
    class Photos:
        def background(name):
            return f'{Paths.backgrounds}/{name}.jpg'
        def specialist(name):
            return f'{Paths.specialists}/{name}.jpg'
        def action(name_with_extension):
            return f'{Paths.actions}/{name_with_extension}'
