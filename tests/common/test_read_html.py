import datetime
import io
import os

import bs4
import pytest

from PPRUNE.common import read_html

@pytest.mark.parametrize(
    'attr, expected',
    (
        ('href', "https://www.pprune.org/members/219249-nicolai"),
        ('name', "nicolai"),
        ('user_id', "219249-nicolai"),
        ('user_int', 219249),
    )
)
def test_user_attributes(attr, expected):
    user = read_html.User(href="https://www.pprune.org/members/219249-nicolai", name="nicolai")
    assert hasattr(user, attr)
    assert getattr(user, attr) == expected


@pytest.mark.parametrize(
    'file_name, expected',
    (
        ('423988-concorde-question-2.html', ('423988', '-concorde-question-', '2')),
        ('423988-concorde-question.html', ('423988', '-concorde-question', None)),
    )
)
def test_user_attributes(file_name, expected):
    match = read_html.RE_FILENAME.match(file_name)
    assert match is not None
    assert match.groups() == expected


# From: https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html
# Content starts with 'Reports on Twitter'
EXAMPLE_PPRINE_PAGE_URL = 'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html'
EXAMPLE_PPRUNE_PAGE = ''
with open(os.path.join(os.path.dirname(__file__), 'example_page.html')) as file:
    EXAMPLE_PPRUNE_PAGE += file.read()


# Example fragment of HTML that is a post
EXAMPLE_SINGLE_PPRUNE_POST = """<div id="posts">
<!-- post #10994338 -->
<div id="edit10994338">
    <!-- this is not the last post shown on the page -->

    <div id="post10994338">
        <div class="tpost">

            <div class="trow-group">
                <div class="trow thead smallfont">
                    <div class="tcell" style="width:175px;">
                        <!-- status icon and date -->
                        <a name="post10994338">
                            <img class="inlineimg" src="https://www.pprune.org/images/statusicon/post_old.gif" alt="Old"/>
                        </a>

                                            20th Feb 2021, 22:11

                                            <!-- / status icon and date -->
                    </div>
                    <div class="tcell text-right">

                                            &nbsp;
                                            #
                        <a href="https://www.pprune.org/10994338-post1.html" target="new" id="postcount10994338" name="1">
                            <strong>1</strong>
                        </a>
                         (
                        <b>
                            <a href="https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338" title="Link to this Post">permalink</a>
                        </b>
                        ) &nbsp;


                    </div>
                </div>

                <div class="trow">
                    <div class="tcell alt2" style="width:175px;">
                        <script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"nicolai","memberOf":"Registered Member","url":"https://www.pprune.org/member.php?u=219249"}</script>
                        <div id="postmenu_10994338">

                            <a rel="nofollow" class="bigusername" href="https://www.pprune.org/members/219249-nicolai">nicolai</a>
                            <script type="2054ed5ceb28d642617005d7-text/javascript">
                            vbmenu_register("postmenu_10994338", true);
                            </script>

                        </div>

                        <div class="smallfont">
                            <span class="alt2 threadstarter">Thread Starter</span>
                        </div>

                        <div class="smallfont">

                                                    &nbsp;
                            <br/>
                            <div>Join Date: Jan 2008</div>
                            <div>Location: It used to be an island...</div>

                            <div>
                                                        Posts: 233
                                                    </div>

                            <div></div>
                        </div>

                    </div>

                    <div class="tcell alt1" id="td_post_10994338">

                        <!-- icon and title -->
                        <div class="smallfont">

                            <strong>United B777 engine failure</strong>
                        </div>
                        <hr/>
                        <!-- / icon and title -->

                        <!-- message -->
                        <div id="post_message_10994338">


                                                    Reports on Twitter that a UAL 777-200 has had an uncontained engine failure on the way from DEN (Denver, Colorado, USA) to HNL (Honolulu, Hawai'i, USA) and returned safely to DEN. Local news report:
                            <a href="https://thepostmillennial.com/colorado-residents-shocked-falling-debris-united-airlines" target="_blank">https://thepostmillennial.com/colora...nited-airlines</a>
                            <br/>
                            <br/>
                             There's a twitter post by user @stillgray with video of the failed engine from in the aircraft that PPRuNe doesn't seem to want to include here...
                            <br/>
                            <br/>
                            <img src="https://cimg6.ibsrv.net/gimg/pprune.org-vbulletin/800x400/1613859028_bfa90ab22ac53d454b9d408b228b58c1bbed57fd.jpeg" alt="" class="post_inline_image"/>
                            <br/>
                            <i>UAL 777</i>
                            <br/>
                            <img src="https://cimg0.ibsrv.net/gimg/pprune.org-vbulletin/2000x1504/eusp_qruuaiubbl_jpeg_3753a703c961585ca56d2e7fcd59348e31d1b385.jpg" alt="" class="post_inline_image"/>
                            <br/>
                            <i>Ground debris</i>
                            <br/>

                        </div>
                        <!-- / message -->

                    </div>
                </div>
                <div class="trow">
                    <div class="tcell alt2">
                        <img class="inlineimg" src="https://www.pprune.org/images/statusicon/user_offline.gif" alt="nicolai is offline"/>

                        <a href="https://www.pprune.org/report.php?p=10994338" rel="nofollow">
                            <img class="inlineimg" src="https://www.pprune.org/images/buttons/report.gif" alt="Report Post"/>
                        </a>


                                            &nbsp;

                    </div>

                    <div class="tcell alt1 text-right">
                        <!-- controls -->

                        <a class="button hollow primary" href="https://www.pprune.org/newreply.php?do=newreply&amp;p=10994338" rel="nofollow">
                            <i class="fas fa-quote-right"></i>
                             Quote
                        </a>

                        <a class="button hollow primary" href="https://www.pprune.org/newreply.php?do=newreply&amp;p=10994338" rel="nofollow" id="qr_10994338" onclick="if (!window.__cfRLUnblockHandlers) return false; return false" data-cf-modified-2054ed5ceb28d642617005d7-="">
                            <i class="fas fa-bolt"></i>
                             Quick Reply
                        </a>

                        <!-- / controls -->
                    </div>
                </div>
            </div>
            <!-- trow-group -->
        </div>
        <!-- tbox -->
    </div>

    <!-- post 10994338 popup menu -->
    <div class="vbmenu_popup" id="postmenu_10994338_menu" style="display:none">
        <div class="tbox">
            <div class="trow thead">
                <div class="tcell">nicolai</div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a rel="nofollow" href="https://www.pprune.org/members/219249-nicolai">View Public Profile</a>
                </div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a href="https://www.pprune.org/private.php?do=newpm&amp;u=219249" rel="nofollow">Send a private message to nicolai</a>
                </div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a href="https://www.pprune.org/search.php?do=finduser&amp;u=219249" rel="nofollow">Find More Posts by nicolai</a>
                </div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a rel="nofollow" href="https://www.pprune.org/profile.php?do=addlist&amp;userlist=buddy&amp;u=219249">Add nicolai to Your Contacts</a>
                </div>
            </div>

        </div>
    </div>
    <!-- / post 10994338 popup menu -->

</div>

<!-- / post #10994338 -->
</div>
<div id="lastpost" />
"""


def test_read_posts_from_example_pprune_page():
    file = io.StringIO(EXAMPLE_PPRUNE_PAGE)
    post_nodes = read_html.get_post_nodes_from_file(file)
    # print(posts)
    assert len(post_nodes) == 20


def test_read_posts_from_example_pprune_post():
    file = io.StringIO(EXAMPLE_SINGLE_PPRUNE_POST)
    post_nodes = read_html.get_post_nodes_from_file(file)
    # print(posts)
    assert len(post_nodes) == 1


def test_html_node_post_id_from_example_pprune_post():
    file = io.StringIO(EXAMPLE_SINGLE_PPRUNE_POST)
    post_nodes = read_html.get_post_nodes_from_file(file)
    assert len(post_nodes) == 1
    result = read_html.html_node_post_id(post_nodes[0])
    assert result == 'edit10994338'


def test_html_node_post_number_from_example_pprune_post():
    file = io.StringIO(EXAMPLE_SINGLE_PPRUNE_POST)
    post_nodes = read_html.get_post_nodes_from_file(file)
    assert len(post_nodes) == 1
    result = read_html.html_node_post_number(post_nodes[0])
    assert result == 10994338


def test_html_node_date_from_example_pprune_post():
    file = io.StringIO(EXAMPLE_SINGLE_PPRUNE_POST)
    post_nodes = read_html.get_post_nodes_from_file(file)
    # print(posts)
    assert len(post_nodes) == 1
    result = read_html.html_node_date(post_nodes[0])
    # print(result)
    assert result == datetime.datetime(2021, 2, 20, 22, 11)


def test_html_node_permalink_from_example_pprune_post():
    file = io.StringIO(EXAMPLE_SINGLE_PPRUNE_POST)
    post_nodes = read_html.get_post_nodes_from_file(file)
    # print(posts)
    assert len(post_nodes) == 1
    result = read_html.html_node_permalink(post_nodes[0])
    # print(result)
    assert result == 'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338'


def test_html_node_user_from_example_pprune_post():
    file = io.StringIO(EXAMPLE_SINGLE_PPRUNE_POST)
    post_nodes = read_html.get_post_nodes_from_file(file)
    # print(posts)
    assert len(post_nodes) == 1
    result = read_html.html_node_user(post_nodes[0])
    print(result)
    assert result.href == 'https://www.pprune.org/members/219249-nicolai'
    assert result.name == 'nicolai'


def test_create_post_objects_from_example_pprune_post():
    file = io.StringIO(EXAMPLE_SINGLE_PPRUNE_POST)
    post_nodes = read_html.get_post_nodes_from_file(file)
    # print(posts)
    assert len(post_nodes) == 1
    post = read_html.post_from_html_node(post_nodes[0])
    print(post)
    assert post is not None
    # text = post.text
    # print(text)
    text_stripped = post.text_stripped
    # print(text_stripped)
    assert text_stripped == """Reports on Twitter that a UAL 777-200 has had an uncontained engine failure on the way from DEN (Denver, Colorado, USA) to HNL (Honolulu, Hawai'i, USA) and returned safely to DEN. Local news report:
https://thepostmillennial.com/colora...nited-airlines
There's a twitter post by user @stillgray with video of the failed engine from in the aircraft that PPRuNe doesn't seem to want to include here...
UAL 777
Ground debris"""


def test_create_post_objects_text_stripped_from_example_pprune_page():
    file = io.StringIO(EXAMPLE_PPRUNE_PAGE)
    post_nodes = read_html.get_post_nodes_from_file(file)
    # print(posts)
    assert len(post_nodes) == 20
    posts = [read_html.post_from_html_node(post_node) for post_node in post_nodes]
    text_stripped = [post.text_stripped for post in posts]
    # print(text_stripped)
    assert len(text_stripped) == 20


# Example of a page with only three posts so no continuation pages.
# https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html
EXAMPLE_PPRUNE_PAGE_THREE_POSTS_URL = 'https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html'
EXAMPLE_PPRUNE_PAGE_THREE_POSTS = ''
with open(os.path.join(os.path.dirname(__file__), 'example_page_three_posts.html')) as file:
    EXAMPLE_PPRUNE_PAGE_THREE_POSTS += file.read()


# Not to burden pytest with huge string identifiers.
PAGE_MAP = {
    0 : EXAMPLE_PPRUNE_PAGE,
    1: EXAMPLE_PPRUNE_PAGE_THREE_POSTS,
}


@pytest.mark.parametrize(
    'url, page_map_index, expected',
    (
            (EXAMPLE_PPRINE_PAGE_URL, 0,
             ['https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-2.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-3.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-4.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-5.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-6.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-7.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-8.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-9.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-10.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-11.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-12.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-13.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-14.html']),
            (EXAMPLE_PPRUNE_PAGE_THREE_POSTS_URL, 1,
             ['https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html']),
    )
)
def test_all_page_urls_from_page(url, page_map_index, expected):
    html_page = read_html.parse_str_to_beautiful_soup(PAGE_MAP[page_map_index])
    result = read_html.all_page_urls_from_page(url, html_page)
    assert result == expected


@pytest.mark.parametrize(
    'url, expected',
    (
            (EXAMPLE_PPRINE_PAGE_URL,
             ['https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-2.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-3.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-4.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-5.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-6.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-7.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-8.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-9.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-10.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-11.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-12.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-13.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-14.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-15.html',
              ]),
            (EXAMPLE_PPRUNE_PAGE_THREE_POSTS_URL,
             ['https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html']),
    )
)
def test_all_page_urls_from_external_url(url, expected):
    html_page = read_html.parse_url_to_beautiful_soup(url)
    result = read_html.all_page_urls_from_page(url, html_page)
    assert result == expected
