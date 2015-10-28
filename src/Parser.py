"""
@author Eric Le Fort
"""
class Parser():
    
    """
     Searches through a String for a certain phrase or term. Returns the starting index for all occurrences of the query String.
     If the query is not located, it will return an empty array.
     @param query - The String we are looking for.
     @param data - The String we are searching through.
     @return Indexes corresponding to the beginning of the location of the String in question.
    """
    def searchForString(query, data):
        locations = [];
        queryIndex = 0;
        
        data.strip();
        query.strip();
        query = query.lower();
        data = data.lower();
        
        # Impossible for data to contain query or query is nonsensical.
        if len(query) > len(data) or len(query) == len(data) or len(query) == 0: 
            return [];
        
        for i in range(0, len(data)):
            if data[i] == query[queryIndex]:  # Current location is matching the query pattern so far.
                if queryIndex == len(query) - 1:  # The whole query pattern is matched, add starting index.
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                else:
                    queryIndex += 1;
                
            else:
                queryIndex = 0;
                
        return locations;
