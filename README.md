arbtt-graph
===========

## arbtt - Automatic Rule Based Time Tracker

**Note: Requires `arbtt-stats` version 0.9, since it has `for-each=minute`, which is required for the barcode chart to work.**

I love [arbtt](http://arbtt.nomeata.de/). Just remember to add `arbtt-capture` to your startup applications and let it record active windows in the background. Then you can use `arbtt-stats` to categorize recorded data. For example, running `arbtt-stats` with the included `categorize.cfg` file:

```sh
$ arbtt-stats --categorizefile=./categorize.cfg -c Graph
Statistics for category "Graph"
===============================
________________Tag_|_________Time_|_Percentage_
Graph:social        | 10d01h18m00s |      11.23
Graph:mail          |  9d04h08m00s |      10.25
Graph:read-pdf      |  6d23h17m00s |       7.79
Graph:term          |  6d17h47m00s |       7.53
Graph:irc           |  2d16h47m00s |       3.02
Graph:tv-local      |  2d08h28m00s |       2.63
Graph:communities   |  2d05h19m00s |       2.48
Graph:write         |  1d17h06m00s |       1.91
(9 entries omitted) |  3d15h44m00s |       4.08
(unmatched time)    | 43d22h02m00s |      49.07
```

It is pretty cool. But you would agree that colored graphs are much more striking than a plain ascii table? So taking a few ideas from [karpathy's](https://github.com/karpathy/) [ulogme](https://github.com/karpathy/ulogme), I wrote this tool to plot my daily stats as logged by `arbtt-capture`.

## Getting Started

### Start recording

1. Install [`arbtt`](http://arbtt.nomeata.de/#install). Run `arbtt-capture` at startup.
2. Probably let it run for some time to have some data.

### Using arbtt-graph

1. Clone/download this repository.
2. Have a look at the `categorize.cfg` file. Add similar categories to your `categorize.cfg` file. (Usually at `~/.arbtt/categorize.cfg`).
3. **Important:** Modify path of the file in `update`.
4. **Important:** Accordingly modify `render/settings.js` for barcode categories.
5. Once everything is set up, run `update` once.
6. Now you can run `./arbtt-server.py` (or `python3 arbtt-serve.py`) and go to the displayed address. (Default: <`http://localhost:9999`>)
7. You can refresh anytime using the reload button to the right.

## Structure

All html/js UI is inside the `render` folder. Also no information other than the percentage usage is inside the `json` files, so you can even make the plots public for extra extrinsic motivation. :smile:

Suggestions and pull requests are always welcome.

## Thanks

- [Joachim Breitner](https://github.com/nomeata) for `arbtt` and numerous suggestions.
- [Andrej Karpathy](https://github.com/karpathy/) for `ulogme`.

> ## Happy tracking!
