def cleanup(body):

	# Recode HTML codes
	body = re.sub("&gt;", ">", body)
	body = re.sub("&lt;", "<", body)
	body = re.sub("&amp;", "&", body)
	body = re.sub("&nbsp;", " ", body)

	# Remove deleted
	body = re.sub("^[deleted]$", "", body)

	# Remove URL
	body = re.sub("http[[:alnum:][:punct:]]*", " ", body) # url

	# Remove /r/subreddit, /u/user
	body = re.sub("/r/[[:alnum:]]+|/u/[[:alnum:]]+", " ", body)

	# Remove quoted comments
	body = re.sub("(>.*?\\n\\n)+", " ", body)

	# Remove control characters (\n, \b)
	body = re.sub("[[:cntrl:]]", " ", body)

	# Remove single quotation marks (contractions)
	body = re.sub("'", "", body)

	# Remove punctuation
	body = re.sub("[[:punct:]]", " ", body)

	# Replace multiple spaces with single space
	body = re.sub("\\s+", " ", body) # Multiple spaces
	# body = re.sub("^\\s+", "", body) # Space at the start of the string
	# body = re.sub("+\\s$", "", body) # Space at the end of the string
	body = body.strip()

	# Lower case
	body = body.lower()

	# Return comment length (number of words) and body (cleaned up text)
	return len(body.split()), body
