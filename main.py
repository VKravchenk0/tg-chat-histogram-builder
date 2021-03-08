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


def trim_results(input):
    result = {}
    j = 1
    for i in input:
        if j >= MEMBERS_NUMBER:
            break
        result[i] = input[i]
        j = j + 1

    return result


def sort_dictionary_by_value(input, reverse=False):
    return dict(sorted(input.items(), key=lambda item: item[1], reverse=reverse))


# Substitute result of telegram chat json export. Tested only with text-only export, without photos/videos etc
with open('result_test.json') as json_file:
    data = json.load(json_file)
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

    # sorting records  by the number of messages
    sorted_dict = sort_dictionary_by_value(result_dict, reverse=True)

    sorted_trimmed_dict = trim_results(sorted_dict)

    for i in sorted_trimmed_dict:
        print(i, sorted_trimmed_dict[i])


    sorted_trimmed_reversed = sort_dictionary_by_value(sorted_trimmed_dict)

    plt.bar(list(sorted_trimmed_reversed.keys()), sorted_trimmed_reversed.values(), color='purple')
    plt.tight_layout()
    plt.ylabel('Кількість повідомлень', fontsize=13)
    plt.show()