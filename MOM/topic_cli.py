from models.Topic import Topic

if __name__ == '__main__':
    Topic.read()
    while True:
        choice = input('1) List all topics\n2) Create new topic\n3) Delete existing topic\n4) Close CLI\n')
        print()
        if choice == '1':
            topics = Topic.list()
            for topic in topics:
                print('-' + topic.name)
        elif choice == '2':
            new_topic = input('Name of new topic: ')
            Topic(new_topic)
            Topic.write()
            print('Topic created succesfully')
        elif choice == '3':
            to_delete = input('Name of topic to delete: ')
            try:
                topic = Topic.topics[Topic.attributesToId(to_delete)]
                topic.delete()
                Topic.write()
                print('Topic deleted succesfully')
            except KeyError:
                print('That topic doesn''t exists')
        elif choice == '4':
            print('Closing...')
            exit()
        else:
            print('Wrong choice!')
        print()