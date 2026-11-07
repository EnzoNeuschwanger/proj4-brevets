import nose
import acp_times
import arrow

brevet_distances = [200, 400, 600, 800, 1000, 1300]

def test_simple_200_times():
    """Tests Opening time for 100 control on 200km brevet"""
    assert acp_times.open_time(100.0, 200.0, arrow.get(0)) == arrow.get(0).shift(hours=(100/34)).isoformat()
    assert acp_times.close_time(100.0, 200.0, arrow.get(0)) == arrow.get(0).shift(hours=(100/15)).isoformat()


def test_complex_times():
    unix_epoc = arrow.get(0)
    #print(acp_times.open_time(890, 1000, unix_epoc))
    #print(unix_epoc.shift(hours=((200/34) + (200/30) + (290)/2)).isoformat())

#Closing Times
    # 890 on a 1000 brevet
    #print(acp_times.close_time(890, 1000, unix_epoc))
    #print(unix_epoc.shift(hours=((600/15) + (290/11.428))).isoformat())
    assert acp_times.close_time(890, 1000, unix_epoc) == unix_epoc.shift(hours=((600/15) + (290/11.428))).isoformat()
    # 350 on a 400 brevet
    assert acp_times.close_time(350, 400, unix_epoc) == unix_epoc.shift(hours=(350/15)).isoformat()
    # 1100 on a 1300 brevet
    assert acp_times.close_time(550, 600, unix_epoc) == unix_epoc.shift(hours=(550/15)).isoformat()

#Opening Times
    # 890 on a 1000 brevet
    assert acp_times.open_time(890, 1000, unix_epoc) == unix_epoc.shift(hours=((200/34) + (200/32) + (200/30) + (290)/28)).isoformat()
    # 350 on a 400 brevet
    assert acp_times.open_time(350, 400, unix_epoc) == unix_epoc.shift(hours=((200/34) + (150/32))).isoformat()
    # 1100 on a 1300 brevet
    assert acp_times.open_time(550, 600, unix_epoc) == unix_epoc.shift(hours=((150/30) + (200/32) + (200/34))).isoformat()


def test_zero_distance_controls():
    """Controls with distance 0km should always produce 00:00 for opening times and 01:00 for closing times"""
    unix_epoc = arrow.get(0)
    assert acp_times.open_time(0, 200, unix_epoc) == unix_epoc.isoformat()
    assert acp_times.close_time(0, 200, unix_epoc) == unix_epoc.shift(hours=1).isoformat()


def test_less_thank_60():
    """For distances less than 60, closing time is calculated as T= (d/20) + 1"""
    unix_epoc = arrow.get(0)
    assert acp_times.close_time(40, 200, unix_epoc) == unix_epoc.shift(hours=((40/20)+1)).isoformat()

def test_finish_line_rules():
    """For 200km brevets, endtime is always 13:30"""
    unix_epoc = arrow.get(0)
    assert acp_times.close_time(200, 200, unix_epoc) == unix_epoc.shift(hours=((13.5))).isoformat()
    """For 400km brevets, endtime is always 27:00"""
    assert acp_times.close_time(400, 400, unix_epoc) == unix_epoc.shift(hours=((27))).isoformat()

def test_time_extend():
    """Brevet length always takes precident for time calculations where distance is larger"""
    unix_epoc = arrow.get(0)
    #Close
    assert acp_times.close_time(205, 200, unix_epoc) == unix_epoc.shift(hours=((13.5))).isoformat()
    assert acp_times.close_time(405, 400, unix_epoc) == unix_epoc.shift(hours=((27.0))).isoformat()
    assert acp_times.close_time(605, 600, unix_epoc) == unix_epoc.shift(hours=((40.0))).isoformat()
    assert acp_times.close_time(1005, 1000, unix_epoc) == unix_epoc.shift(hours=((600/15 + 400/11.428))).isoformat()

    #Open
    assert acp_times.open_time(205, 200, unix_epoc) == unix_epoc.shift(hours=((200/34))).isoformat()
    assert acp_times.open_time(405, 400, unix_epoc) == unix_epoc.shift(hours=((200/34) + (200/32))).isoformat()
    assert acp_times.open_time(605, 600, unix_epoc) == unix_epoc.shift(hours=((200/34) + (200/32) + (200/30))).isoformat()
    assert acp_times.open_time(1005, 1000, unix_epoc) == unix_epoc.shift(hours=((200/34) + (200/32) + (200/30) + (400/28))).isoformat()


def test_bad_values():
    """Testing for wrong inputs"""
    unix_epoc = arrow.get(0)
    assert acp_times.close_time(-1, 200, unix_epoc) == "NEGATIVE_DISTANCE" 
    assert acp_times.close_time(100, 2001, unix_epoc) == "INCORRECT_BREVET"

    assert acp_times.open_time(-1, 200, unix_epoc) == "NEGATIVE_DISTANCE" 
    assert acp_times.open_time(100, 2001, unix_epoc) == "INCORRECT_BREVET"
