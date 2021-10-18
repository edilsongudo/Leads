from django.core import management


def schedule_db_backup():

    with open('databasebackup.json', 'w') as f:
        try:
            management.call_command(
                'dumpdata',
                '--indent=4',
                '--natural-foreign',
                '--natural-primary',
                '-e=contenttypes',
                '-e=admin.logentry',
                '-e=sessions',
                '-e=auth.Permission', stdout=f)
        except Exception as e:
            print(e)

    print('Backup done')
