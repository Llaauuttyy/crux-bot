from show_posts import posts_reader


def date_transforming(posts_info_list):

    # PRE: Receives posts_info_list which is
    # a dictionary list filled up with posts data.

    # POST: Seaches the date and time and transforms them
    # in order to print them right after.

    for post in range(len(posts_info_list)):

        for key in posts_info_list[post]:

            if key == "updated_time":
                date_and_time = posts_info_list[post]["created_time"]
                used_date, complete_hour = date_and_time.split("T")
                splitted_hour = complete_hour.split("+")
                used_time = splitted_hour[0]
                print(f"Date: {used_date}. Time: {used_time}.")

                # Time's been caught from Facebook servers (Different than ours).


def main():
    # Use the function that was
    # imported at the start of the file.
    posts_info_list = posts_reader()
    date_transforming(posts_info_list)


main()

# Comments amount could also be printed if it wanted
