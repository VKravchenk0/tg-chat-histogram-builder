import json
import matplotlib
import matplotlib.pyplot as plt
import emoji

font = {'family': 'normal',
        'size': 9}
matplotlib.rc('font', **font)

# number of members to be included in the plot
MEMBERS_NUMBER = 35


def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(r'', text)


# Substitute result of telegram chat json export. Tested only with text-only export, without photos/videos etc
with open('result_test.json') as json_file:
    data = json.load(json_file)
    result_dict = {}
    for message in data["messages"]:
        if "from" not in message or message["from"] is None:
            continue

        from_field = remove_emoji(message["from"])
        if from_field not in result_dict:
            # add a new record
            result_dict[from_field] = 1
        else:
            # increment
            result_dict[from_field] = result_dict[from_field] + 1

    # sorting records  by the number of messages
    sorted_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))

    sorted_trimmed_dict = {}
    j = 1
    for i in sorted_dict:
        if (j >= MEMBERS_NUMBER):
            break
        sorted_trimmed_dict[i] = sorted_dict[i]
        j = j + 1

    for i in sorted_trimmed_dict:
        print(i, sorted_trimmed_dict[i])

    sorted_trimmed_reversed = dict(sorted(sorted_trimmed_dict.items(), key=lambda item: item[1]))

    print("---------------------------------------")

    for i in sorted_trimmed_reversed:
        print(i, sorted_trimmed_reversed[i])

    with_new_lines = {}
    for i in sorted_trimmed_reversed:
        with_new_lines[i.replace(' ', '\n')] = sorted_trimmed_reversed[i]

    print("---------------------------------------")

    for i in with_new_lines:
        print(i, with_new_lines[i])


    plt.bar(list(with_new_lines.keys()), with_new_lines.values(), color='purple')
    plt.tight_layout()
    plt.ylabel('Кількість повідомлень', fontsize=13)
    plt.show()