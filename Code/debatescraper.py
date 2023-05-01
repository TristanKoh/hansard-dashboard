
# TODO: Abstract the structure of the scraping into a separate class
"""
We now need to tag the speaker's name to what they said: One column for the name and the other for the text

We use two lists, one with the para_text, the other as MP tag that is the same length as para_text:
In the end we will get a dataframe, one column with the MP tag, and the other with the text. 
Each row corresponds with a paragraph, and each paragraph will be labelled with the MP's name.

Implementation:
Since para_text contains the text of the MP denoted with <strong>, we save the indices of those in para_text with <strong> 
in a separate list tag_bold.

We then initialise the MP tag list that is same length as para_text and loop over the this list
If the index is in tag_bold, we know that this paragraph has a new speaker, and hence we write the speaker's name to the equivalent index
in the names list. 

We maintain a counter that increments by one everytime there is a match between the tag_bold and index, 
because the bolded list does not have empty strings and is a different length from the para_text list.
But the bolded list lists names in chronological order (ie in the order in which they speak), and hence we can follow the chronology of the
speeches as well.

We can then forward fill the empty strings with the most recent MPs name in the column.
"""

def tagged_mp_name_to_text(self, bolded_text, para_text) :
    
    # Check the para_text list for the indices where there is <bold>: This means that there is a new speaker for that paragraph
    tag_bold = []
    for index, para in enumerate(para_text):
        if "<strong>" in para.get_attribute('innerHTML'):
            tag_bold.append(index)


    # Maintain a counter for the index of bolded that starts at 1 (since the first bolded element is the name of the debat)
    # Loop over para_text, check if the index is in tag_bold.
    # If it is, insert the relevant name from the bolded list at the current index
    # If not, don't do anything

    names = [""] * len(para_text)
    bolded_counter = 1

    for index, para in enumerate(para_text):
        
        if index in tag_bold:
            names[index] = bolded_text[bolded_counter].text
            bolded_counter += 1
        
        elif index not in tag_bold :
            pass
    
    return names, [para.text for para in para_text]
        
            