import json

# Load the street data from your provided JSON
with open('test3.json', 'r', encoding='utf-8') as f:
    street_data = json.load(f)


def find_best_street_match(street_name, street_data):
    # Split the input street name and take the longest word
    street_words = street_name.split()
    street_words.sort(key=len, reverse=True)
    longest_word = street_words[0]

    # Function to try and match based on the word variations
    def try_match(street_list, word):
        # Exact match first
        matches = [street for street in street_list if word in street['street_name_ka']]
        if matches:
            return matches

        # Try matching by shortening the word progressively from the end
        for i in range(1, len(word) + 1):
            shortened_word = word[:-i]
            matches = [street for street in street_list if shortened_word in street['street_name_ka']]
            if matches:
                return matches
        return None

    # Try to match with the longest word and then with progressively shortened word
    match = try_match(street_data, longest_word)

    if match:
        return match
    else:
        return f"No match found for {street_name}"


# Example usage
street_name = "გელოვანი არჩილის ქუჩა"
best_match = find_best_street_match(street_name, street_data)
print(best_match)
