**This is a recursive function that takes main folder as a first argument and file formats to be extracted as the other arguments**
Because the function is recursive it doesn't matter how deeply nested the specified directory is.  <br>
2 argument onwards are all the file formats you want to check for.
Since I check if any of the "file formats" are in any of the file names, it can be not only formats but really any partial string you want to search for in a file name.
