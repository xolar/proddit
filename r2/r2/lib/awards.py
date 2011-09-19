# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is Reddit.
#
# The Original Developer is the Initial Developer.  The Initial Developer of the
# Original Code is CondeNet, Inc.
#
# All portions of the code written by CondeNet are Copyright (c) 2006-2010
# CondeNet, Inc. All Rights Reserved.
################################################################################

from r2.lib.promote import *
"""
And the winners are...
"""

def give_awards():
    import re
    from r2.models import Account, Subreddit, Award
    from r2.lib import utils
    from datetime import datetime, timedelta

    
    q = Account._query(Account.c._spam == False,
                       Account.c._deleted == False,
                       sort = asc('_date'),
                       #Account.c.link_karma>-1,
                       limit = 1000,
                       data = True)
    

    i=0
    ctime = datetime.now(g.tz)
    for account in utils.fetch_things2(q):
        prev_visit = last_visit(account)
        if not prev_visit:
            print "%s hasn't logged in for a long time" % account.name
            continue
        if (ctime - prev_visit).days > 90:
            print "%s hasn't logged in for %d days" % (account.name,(ctime-prev_visit).days)
            continue
        tsince = ctime - account._date
        if tsince.days < 30:
            Award.give_if_needed("newbie", account)
        elif tsince.days >= 30:
            Award.take_away("newbie", account)
        if tsince.days >= 365 and tsince.days < 365*2:
            Award.give_if_needed("1year", account)
        elif tsince.days >= 365*2:
            Award.take_away("1year", account)
            Award.give_if_needed("2years", account)
        if account.email_verified:
            print "%s has verified email: %s" % (account.name,account.email)
            Award.give_if_needed("verified_email", account)

def post_user_stats():
    import re
    from r2.models import Account, Subreddit, Award
    from r2.lib import utils
    from datetime import datetime, timedelta

    
    q = Account._query(sort = asc('_date'),
                       limit = 1000,
                       data = True)
    

    spammers=0
    deleted=0
    prev_visited=0
    total=0
    ctime = datetime.now(g.tz)
    for account in utils.fetch_things2(q):
        print "\n-------------------------------------"
        print account.name
        print account._spam
        print account._deleted
        total+=1
        prev_visit = last_visit(account)
        if not prev_visit:
            print "%s hasn't logged in for a long time" % account.name
            prev_visited+=1
        else:
            tsince = ctime - prev_visit
            if tsince.days > 10:
                prev_visited+=1
            print "%s hasn't logged in for %d days" % (account.name,tsince.days)

        if  account._spam:
            print "%s is a spammer and banned " % account.name
            spammers+=1
        if  account._deleted:
            print "%s has deleted his/her account " % account.name
            deleted+=1
    print "there are %d deleted accounts, %d spammers, %d haven't logged in in a long time from a total of %d. so there are %d more valid users" % (deleted,spammers,prev_visited,total,total-spammers-deleted-prev_visited)
