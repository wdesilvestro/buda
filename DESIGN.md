# Designing BUDA

## *What's the Inspiration?*
To start, I think it's best to sure what my inspiration was for the Bulk Uniform Document Analyzer. This past semester, I've served as a member on the Institute of Politics' Technology & Innovation Committee. We've been researching how historical districts throughout Massachusetts affect the adoption of solar energy. Part of my job has been to go through the publicly released meeting minutes and agendas from the historic district commissions throughout the state. I quickly found this frustrating though, as there are hundreds of these documents and I felt there should be a better way to standardize this process. Thus, BUDA was born!

## A Recursive Solution
Of the 30+ hours that was put into implementing BUDA, at least 20 of that was dedicated to devising the recursive solution. This is most prominently seen in the `joint_parse()` and `parse_tree()` functions of the `library.py` file. `parse_tree()` is where almost 80% of the processing involved with BUDA actually happens.

When I was setting out to design BUDA, I was trying to think of a way to generalize it to work on any sort of document. This necessitated avoiding any sort of hardcoded limits on the nesting depth (e.g. record within a record within a container and so on) and just providing for general flexibility with the templates that users provided. I ultimately looked towards recursion because it allowed for a way for BUDA to step through the template file and gradually parse an infinite number of levels for it. It took an incredible amount of time to figure out how to implement this solution, but it's far more elegant than any other alternative I could think of.

In essence, `joint_parse()` is a handler function that deals with the file I/O aspects of the program. It passes the XML template and document to `parse_tree()`, which continually calls itself until it's processed down to the base case, which is an element. This solution is adaptable, flexible, and worked great for what I wanted.

## Deciding on a Template Language
I was quite conflicted on what the templates that the user provided would look like. While XML is perhaps not the most user-friendly and comes with a learning curve, it was the best in terms of the tradeoff of programming time vs. difficult of template creation. I also looked towards creating my own language (which would have been too time consuming) or using HTML or some other language (most of which were too loose and not strict enough for my purposes.)

The key advantage of choosing XML is that Python comes with its own built-in XML processor, which made parsing the XML templates significantly easier than any other solution would have allowed for. `xml.etree` made BUDA efficient and responsive to the XML templates and was a great tool to use in this project.

## Choosing an Export Format
Initially, I wanted to export the files in CSV format. I ended up opting for JSON files instead because that allowed for the files to not be flat, but rather hierarchical in nature. While CSV has greater interoperability and ubiquity than JSON, it lacks the ability to express equally complex data. Thus, it made sense to use JSON for BUDA. Python has great libraries to handle JSON natively and made this process very easy for me.