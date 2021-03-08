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


def normalize_from_field(input):
    """
    Removes emoji and adds new lines between words in order for the text to look better on the plot
    """
    return remove_emoji(input).replace(' ', '\n')


def build_username_messages_count_dictionary(data):
    """
    Builds a dictionary with username as a key and number of messages from this user as a value
    :param data: json data with telegram chat export results
    """
    result_dict = {}
    for message in data["messages"]:
        if "from" not in message or message["from"] is None:
            continue

        from_field = normalize_from_field(message["from"])
        if from_field not in result_dict:
            # add a new record
            result_dict[from_field] = 1
        else:
            # increment
            result_dict[from_field] = result_dict[from_field] + 1

    return result_dict


def trim_members(input):
    """
    Returns the last MEMBERS_NUMBER records from the input dictionary
    """
    input_length = len(input)
    last_n_results = list(input.items())[input_length - MEMBERS_NUMBER: input_length]
    result = {}
    for item in last_n_results:
        result[item[0]] = item[1]

    return result


def sort_dictionary_by_messages_count(input):
    return dict(sorted(input.items(), key=lambda item: item[1]))


def show_histogram(input_dict):
    plt.bar(list(input_dict.keys()), input_dict.values(), color='purple')
    plt.tight_layout()
    plt.ylabel('Кількість повідомлень', fontsize=13)
    plt.show()


# Substitute result of telegram chat json export. Tested only with text-only export, without photos/videos etc
with open('result.json') as json_file:
    data = json.load(json_file)

    all_members_dict = build_username_messages_count_dictionary(data)

    sorted_dict = sort_dictionary_by_messages_count(all_members_dict)

    sorted_trimmed_dict = trim_members(sorted_dict)

    show_histogram(sorted_trimmed_dict)