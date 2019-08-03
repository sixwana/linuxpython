    ___    __                 _ __  __                 __           ___              _                                  __     ___ 
   /   |  / /___ _____  _____(_) /_/ /_  ____ ___     / /_____     /   |  __________(_)___ _____  ____ ___  ___  ____  / /_   |__ \
  / /| | / / __ `/ __ \/ ___/ / __/ __ \/ __ `__ \   / __/ __ \   / /| | / ___/ ___/ / __ `/ __ \/ __ `__ \/ _ \/ __ \/ __/   __/ /
 / ___ |/ / /_/ / /_/ / /  / / /_/ / / / / / / / /  / /_/ /_/ /  / ___ |(__  |__  ) / /_/ / / / / / / / / /  __/ / / / /_    / __/ 
/_/  |_/_/\__, /\____/_/  /_/\__/_/ /_/_/ /_/ /_/   \__/\____/  /_/  |_/____/____/_/\__, /_/ /_/_/ /_/ /_/\___/_/ /_/\__/   /____/ 
         /____/                                                                    /____/                                          


# Final goal:
Generate a daily, weekly, and monthly report on the amount of time
users were logged in.

    ____                  __ 
   /  _/___  ____  __  __/ /_
   / // __ \/ __ \/ / / / __/
 _/ // / / / /_/ / /_/ / /_  
/___/_/ /_/ .___/\__,_/\__/  
         /_/                 


# 1 - User will provide arguments and filename.

# 2 - Open from a file containing the raw usage data.

    ____                                 _            
   / __ \_________  ________  __________(_)___  ____ _
  / /_/ / ___/ __ \/ ___/ _ \/ ___/ ___/ / __ \/ __ `/
 / ____/ /  / /_/ / /__/  __(__  |__  ) / / / / /_/ / 
/_/   /_/   \____/\___/\___/____/____/_/_/ /_/\__, /  
                                             /____/   

# 3 - Check if each list element has 15 elements:

# 4 - Create a list for each element list. If a specific user or IP is detected in the Input, take into consideration only entries that match the queue.

# 5 - Check if login and logout day is the same or not, if so duplicate the record.

# 6 - Transform login and logout time to seconds

# 7 - Convert list to dictionary containing {user ,pts ,ip, day, month, year, finalSeconds}

# 8 - Add seconds from each day to a new dictionary containing records from 0 to 366 (relative to the amount of days in a year)

   ____        __              __ 
  / __ \__  __/ /_____  __  __/ /_
 / / / / / / / __/ __ \/ / / / __/
/ /_/ / /_/ / /_/ /_/ / /_/ / /_  
\____/\__,_/\__/ .___/\__,_/\__/  
              /_/                 

# 9 - generate daily, weekly and monthly FROM #8

