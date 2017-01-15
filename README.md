# pprune-concorde

There is a [famous thread](http://www.pprune.org/tech-log/423988-concorde-question.html) on pprune.org by Concorde experts that gives an extradinary insight into that aircraft. This is a re-mix of that thread that organises it by subject matter. I hope that it will be easier to read and will spark further interest, and contributions, of that unique aircraft.

Here is the result with the original posts organised into [all 144 subjects](https://paulross.github.io/pprune-concorde/docs/index.html)


# How This was Done
# Why?
Please realise that this is a a fairly 'dumb' mechanical re-ordering of this Concorde thread. My hope is that my work might lead to a much better grouping of Concorde knowledge and stories to be done by others. I feel that it important to retain this information and make it accessible to others.

## Concept

The basic idea was to remove all the common English words from each post and the remaining words give some indication of the subject of the post. The posts could then automatically be reorganised by subject (maintaining the order of posts).

## Practice

In practice this turned out about right but some refinements were needed (for example user names in post would appear as 'interesting words'). After a bit of fiddling around the following techniques seemed to give a good result:

* Strip all punctuation then make all mixed case words lower case. Then eliminate common words. So 'Re-Heat' becomes 'reheat' and that is an unusual word and merits being part of a subject, say "Afterburner/Re-Heat".
* Strip all punctuation then remove all words that were _not_ all upper case. So 'LHR-JFK' becomes 'LHRJFK', an unusual word, and merits being part of a subject, say "LHR-JFK Route".
* Two word phrases were useful. Strip all punctuation then make all mixed case words lower case. Then look at word pairs. So ('rolls', 'royce') clearly is the subject "Rolls Royce". Three word phrases were tried but did not seem to add much.

## Implementation

In the end a manual table was constructed for each of the three techniques, this table mapped the result of the method to a subject name. These tables are in `concorde_pub_map.py` and control how the output is produce from the input.


## Setup

To reproduce this follow these steps on Linux or Mac OS X. I'm afraid Windows users you are on your own.

### Initial Setup

You need [Python 3](https://www.python.org/) installed, I'm using Python 3.6 here. Create a new Python environment (I'm assuming your virtual environments directory is `~/venvs/`):

```
$ python3.6 -m venv ~/venvs/pprune
$ . venvs/pprune/bin/activate
```

Install [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for parsing the HTML:

```
(pprune) $ pip install beautifulsoup4
```

Create a working area and clone the repository:

```
$ mkdir ~/pprune
$ cd ~/pprune
$ git clone https://github.com/paulross/pprune-concorde.git
```

Make a directory for the HTML pages of the thread:

```
$ mkdir original
$ cd original
```

### Get the Original Thread

Grab the first page:

```
$ curl http://www.pprune.org/tech-log/423988-concorde-question.html -o "423988-concorde-question-1.html"

[1/97]: http://www.pprune.org/tech-log/423988-concorde-question.html --> 423988-concorde-question.html
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  126k    0  126k    0     0   148k      0 --:--:-- --:--:-- --:--:--  148k
```
And all the rest:

```
$ curl http://www.pprune.org/tech-log/423988-concorde-question-[2-98].html -o "423988-concorde-question-#1.html"

[1/97]: http://www.pprune.org/tech-log/423988-concorde-question-2.html --> 423988-concorde-question-2.html
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  126k    0  126k    0     0   148k      0 --:--:-- --:--:-- --:--:--  148k
...
[2/97]: http://www.pprune.org/tech-log/423988-concorde-question-3.html --> 423988-concorde-question-3.html
100  124k    0  124k    0     0   223k      0 --:--:-- --:--:-- --:--:--  223k
```

### Process the Original Thread


Head for the source code:

```
$ cd ~/pprune/pprune-concorde/src
```

### Do Some Research

If you want to explore the thread in a programtic way then the `research.py` script is the one for you:

```
(pprune) $ python3.6 research.py ../../original/
```

This will dump out word counts and various other stuff that will allow you to tailor the `concorde_pub_map.py` that controls how the final site is produced.

### Generate the New Pages

Run `main.py` with the location of the pages that you have just pulled down. This will create the output in `~/pprune/pprune-concorde/docs`:

```
(pprune) $ python3.6 main.py ../../original/
Read: /Users/paulross/Documents/workspace/pprune/in/original/423988-concorde-question-1.html posts: 20
Read: /Users/paulross/Documents/workspace/pprune/in/original/423988-concorde-question-2.html posts: 20
Read: /Users/paulross/Documents/workspace/pprune/in/original/423988-concorde-question-3.html posts: 20
...
Read: /Users/paulross/Documents/workspace/pprune/in/original/423988-concorde-question-98.html posts: 12
Read 1942 posts
Number of words: 292355
Reading words file: count_1w.txt
Output path: /Users/paulross/Documents/workspace/pprune/github/pprune-concorde/docs
Writing: index.html
Writing: "ADC (Air Data Computer)"
Writing: "AFCS (Automtic Flight Control System)"
Writing: "AICS (Air Intake Control System)"
Writing: "AICU (Air Intake Control Computer)"
Writing: "ALT HOLD"
Writing: "APU (Auxiliary Power Unit)"
...
Writing: "Vortex AoA"
Bye, bye!
```

Open up the index page:

```
$ open ../docs/index.html
```

# Reference

This describes the source code used to create the final site.

### `read_html.py`

This reads all of the static HTML that comprises the thread, in particlular this produces a `Thread` object that contains an ordered list of `Post` objects. Both of these classes provide an API that makes the subsequent work convenient.

### `analyse_thread.py`

This provides various functions fo analysing the thread or individual posts such as word matching, counting popular words or phrases.

### `research.py`

This has various ad-hoc functions to read the whole thread and dump out the results of an analysis. These results are informative when deciding the `concorde_pub_map.py `.

### `concorde_pub_map.py`

This is a series of dictionaries that map words and phrases to subject titles. These are the heart of converting the original thread to subjects.

### `write_html.py`

This takes the publication map and converts it to the new structure. The code makes two passes over the data:

1. Each post is anlysed in order for the subjects it might refer to. These are added to a subject map which looks like: `{subject : [post_number, ...], ...}`
2. This subject map is then iterated across in subject order, each subject is a set of pages and consists of the list of `[post_number, ...]` from the original material. Pages are limited to 20 posts. Of course each subject is an entry in the `index.html` table.

### `styles.py`

This just contains the CSS styles used in the final result.

### `main.py`

This just brings the whole thing together and generates the output from the input. It is invoked thus:

```
$ python3 main.py <path_to_input>
```
This will write the output to the `../docs` directory.


# Credits

* pprune contributors, there is a hall of fame on [the index page](https://paulross.github.io/pprune-concorde/docs/index.html)
* [Peter Norvig](http://norvig.com/ngrams/) for the most common English words file.
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for their fabulous HTML parser and, of course, [Python](https://www.python.org/).

