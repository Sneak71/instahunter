import click
import requests
import json
from datetime import datetime


@click.group()
def cli():
    """Made by KSSBro | v1.4"""


@click.command()
@click.option('-tag', prompt="Hashtag", help="The hashtag you want to search the posts with")
@click.option('-create-file', default="false", help="true: Create a file with the data | false: Will not create a file, false is default")
@click.option('--file-type', default="text", help="json: Create a json file | text: Create a text file, text is default")
def getposts(tag, create_file, file_type):
    """This command will fetch recent public posts with a Hashtag"""
    try:
        # Creating file if required, creating array json_data to store data if the file type is json
        if(create_file == "true"):
            if(file_type == "json"):
                file = open(tag+"_posts.json", "w+")
                json_data = []
            else:
                file = open(tag+"_posts.txt", "w+", encoding="utf-8")
        counter = 0
        api_url = "https://www.instagram.com/explore/tags/%s/?__a=1" % tag
        req = requests.get(url=api_url)
        data = req.json()
        edges = data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        # Looping through 'edges' in the data acquired
        for edge in edges:
            counter = counter + 1
            # Collecting necessary data from each edge
            try:
                caption = edge["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            except:
                caption = "No Caption"
            scraped_data = {
                "id": counter,
                "post_id": edge["node"]["id"],
                "shortcode": edge["node"]["shortcode"],
                "owner_id": edge["node"]["owner"]["id"],
                "display_url": edge["node"]["display_url"],
                "caption": caption,
                "time": str(datetime.fromtimestamp(
                    edge["node"]["taken_at_timestamp"])),
                "n_likes": edge["node"]["edge_liked_by"]["count"],
                "n_comments": edge["node"]["edge_media_to_comment"]["count"],
                "is_video": edge["node"]["is_video"]
            }
            if(create_file == "true"):
                # If the file type is json then appending the data to json_data array instead of writing it to the file right away
                if(file_type == "json"):
                    json_data.append(scraped_data)
                else:
                    file.write("###############################\nID: %s \nPost ID: %s \nShortcode: %s \nOwner ID: %s \nDisplay URL: %s \nCaption: %s \nTime: %s \nNumber of likes: %s \nNumber of comments: %s \nIs Video: %s \n###############################\n\n\n\n\n" % (
                        str(counter), str(scraped_data["post_id"]), str(scraped_data["shortcode"]), str(scraped_data["owner_id"]), str(scraped_data["display_url"]), str(scraped_data["caption"]), str(scraped_data["time"]), str(scraped_data["n_likes"]), str(scraped_data["n_comments"]), str(scraped_data["is_video"])))
            else:
                click.echo("###############################\nID: %s \nPost ID: %s \nShortcode: %s \nOwner ID: %s \nDisplay URL: %s \nCaption: %s \nTime: %s \nNumber of likes: %s \nNumber of comments: %s \nIs Video: %s \n###############################\n\n\n\n\n" % (
                        counter, scraped_data["post_id"], scraped_data["shortcode"], scraped_data["owner_id"], scraped_data["display_url"], scraped_data["caption"], scraped_data["time"], scraped_data["n_likes"], scraped_data["n_comments"], scraped_data["is_video"]))
        if(create_file == "true"):
            # Closing the file and dumping the data before closing if the file type is json
            if(file_type == "json"):
                json.dump(json_data, file)
                click.echo("File Created, name: '%s_posts.json'" % tag)
            else:
                click.echo("File Created, name: '%s_posts.txt" % tag)
            file.close()
        else:
            click.echo("Done!")
    except:
        click.echo(
            "Couldn't retrieve data, One of the following was the issue: \n1. Your query was wrong \n2. Instagram servers did not respond \n3. There is a problem with your internet connection")


@click.command()
@click.option('-via', prompt="Via", default="username", help="username: search user by Username | id: search user by ID")
@click.option('--value', prompt="Value", help='Username or ID you want to search the user by')
@click.option('-create-file', default="false", help="true: Create a file with the data | false: Will not create a file, false is default")
@click.option('--file-type', default="text", help="json: Create a json file | text: Create a text file, text is default")
def getuser(via, value, create_file, file_type):
    """This command will fetch user data with a Username or ID"""
    # Setting the api url depending upon the user's choice
    if(via == "id"):
        api_url = "https://i.instagram.com/api/v1/users/%s/info" % value
    elif(via == "username"):
        api_url = "https://www.instagram.com/%s/?__a=1" % value
    try:
        req = requests.get(url=api_url)
        data = req.json()
        # Collecting necessary data
        if(via == "id"):
            user = data["user"]
            profile_pic_url = user["hd_profile_pic_url_info"]["url"]
            uploads = user["media_count"]
            followers = user["follower_count"]
            following = user["following_count"]
            tags_following = user["following_tag_count"]
            igtv_videos = user["total_igtv_videos"]
            tagged = user["usertags_count"]
            has_highlights = user["has_highlight_reels"]
            user_id = user["pk"]
        elif(via == "username"):
            user = data["graphql"]["user"]
            profile_pic_url = user["profile_pic_url_hd"]
            uploads = user["edge_owner_to_timeline_media"]["count"]
            followers = user["edge_followed_by"]["count"]
            following = user["edge_follow"]["count"]
            tags_following = "Search by ID!"
            igtv_videos = user["edge_felix_video_timeline"]["count"]
            tagged = "Search by ID!"
            if(user["highlight_reel_count"] > 0):
                has_highlights = True
            else:
                has_highlights = False
            user_id = user["id"]
        scraped_data = {
            "user_id": user_id,
            "username": user["username"],
            "full_name": user["full_name"],
            "profile_pic_url": profile_pic_url,
            "bio": user["biography"],
            "n_uploads": uploads,
            "n_followers": followers,
            "n_following": following,
            "is_private": user["is_private"],
            "is_verified": user["is_verified"],
            "tags_following": tags_following,
            "external_url": user["external_url"],
            "igtv_videos": igtv_videos,
            "n_tagged": tagged,
            "has_highlights": has_highlights
        }
        if(create_file == "true"):
            if(file_type == "json"):
                file = open(value+"_user.json", "w+")
                json.dump(scraped_data, file)
                file.close()
                click.echo("File Created, name: '%s_user.json'" % str(value))
            else:
                file = open(value+"_user.txt", "w+", encoding="utf-8")
                file.write("User ID: %s \nUsername: %s \nFull Name: %s \nProfile Pic URL: %s \nBio: %s \nUploads: %s \nFollowers: %s \nFollowing: %s \nPrivate ID: %s \nVerified ID: %s \nTags following: %s \nExternal URL: %s \nIGTV videos: %s \nTimes user was tagged: %s \nHas highlights: %s" % (
                    str(scraped_data["user_id"]), scraped_data["username"], scraped_data["full_name"], scraped_data["profile_pic_url"], scraped_data["bio"], str(scraped_data["n_uploads"]), str(scraped_data["n_followers"]), str(scraped_data["n_following"]), str(scraped_data["is_private"]), str(scraped_data["is_verified"]), str(scraped_data["tags_following"]), scraped_data["external_url"], str(scraped_data["igtv_videos"]), str(scraped_data["n_tagged"]), str(scraped_data["has_highlights"])))
                file.close()
                click.echo("File Created, name: '%s_user.txt'" % str(value))
        else:
            click.echo("User ID: %s \nUsername: %s \nFull Name: %s \nProfile Pic URL: %s \nBio: %s \nUploads: %s \nFollowers: %s \nFollowing: %s \nPrivate ID: %s \nVerified ID: %s \nTags following: %s \nExternal URL: %s \nIGTV videos: %s \nTimes user was tagged: %s \nHas highlights: %s" % (
                    str(scraped_data["user_id"]), scraped_data["username"], scraped_data["full_name"], scraped_data["profile_pic_url"], scraped_data["bio"], str(scraped_data["n_uploads"]), str(scraped_data["n_followers"]), str(scraped_data["n_following"]), str(scraped_data["is_private"]), str(scraped_data["is_verified"]), str(scraped_data["tags_following"]), scraped_data["external_url"], str(scraped_data["igtv_videos"]), str(scraped_data["n_tagged"]), str(scraped_data["has_highlights"])))
            click.echo('Done!')
    except:
        click.echo(
            "Couldn't retrieve data, One of the following was the issue: \n1. Your query was wrong \n2. Instagram servers did not respond \n3. There is a problem with your internet connection")


@click.command()
@click.option('-username', prompt="Username", help='The username of the user you want to search the user id of')
@click.option('-create-file', default="false", help="true: Create a file with the data | false: Will not create a file, false is default")
@click.option('--file-type', default="text", help="json: Create a json file | text: Create a text file, text is default")
def getuserposts(username, create_file, file_type):
    """This command will fetch recent posts of a user with a Username"""
    try:
        # Creating file if required, creating array json_data to store data if the file type is json
        if(create_file == "true"):
            if(file_type == "json"):
                file = open(username+"_posts.json", "w+")
                json_data = []
            else:
                file = open(username+"_posts.txt", "w+", encoding="utf-8")
        counter = 0
        api_url = "https://www.instagram.com/%s/?__a=1" % username
        req = requests.get(url=api_url)
        data = req.json()
        posts = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
        # Looping through posts
        for post in posts:
            counter = counter + 1
            node = post["node"]
            # Collecting necessary data    
            try:
                caption = node["edge_media_to_caption"]["edges"][0]["node"]["text"]
            except:
                caption = ""
            try:
                location = node["location"]["name"]
            except:
                location = "No Location"
            scraped_data = {
                "id": counter,
                "post_id": node["id"],
                "shortcode": node["shortcode"],
                "display_url": node["display_url"],
                "height": node["dimensions"]["height"],
                "width": node["dimensions"]["width"],
                "caption": caption,
                "time": str(datetime.fromtimestamp(node["taken_at_timestamp"])),
                "n_likes": node["edge_liked_by"]["count"],
                "comments_disabled": node["comments_disabled"],
                "n_comments": node["edge_media_to_comment"]["count"],
                "location": location,
                "is_video": node["is_video"]
            }     
            if(create_file == "true"):
                if(file_type == "json"):
                    # If the file type is json then appending the data to json_data array instead of writing it to the file right away
                    json_data.append(scraped_data)
                else:
                    file.write("###############################\nID: %s \nPost ID: %s \nShortcode: %s \nDisplay URL: %s \nImage Height: %s \nImage Width: %s \nCaption: %s \nTime: %s \nNumber of likes: %s \nComments Disabled: %s \nNumber of comments: %s \nLocation: %s \nIs Video: %s \n###############################\n\n\n\n\n" % (
                        str(counter), str(scraped_data["post_id"]), str(scraped_data["shortcode"]), str(scraped_data["display_url"]), str(scraped_data["height"]), str(scraped_data["width"]), str(scraped_data["caption"]), str(scraped_data["time"]), str(scraped_data["n_likes"]), str(scraped_data["comments_disabled"]), str(scraped_data["n_comments"]), str(scraped_data["location"]), str(scraped_data["is_video"])))
            else:
                click.echo("###############################\nID: %s \nPost ID: %s \nShortcode: %s \nDisplay URL: %s \nImage Height: %s \nImage Width: %s \nCaption: %s \nTime: %s \nNumber of likes: %s \nComments Disabled: %s \nNumber of comments: %s \nLocation: %s \nIs Video: %s \n###############################\n\n\n\n\n" % (
                        str(counter), str(scraped_data["post_id"]), str(scraped_data["shortcode"]), str(scraped_data["display_url"]), str(scraped_data["height"]), str(scraped_data["width"]), str(scraped_data["caption"]), str(scraped_data["time"]), str(scraped_data["n_likes"]), str(scraped_data["comments_disabled"]), str(scraped_data["n_comments"]), str(scraped_data["location"]), str(scraped_data["is_video"])))
        if(create_file == "true"):
            # Closing the file and dumping the data before closing if the file type is json
            if(file_type == "json"):
                json.dump(json_data, file)
                click.echo("File Created, name: '%s_posts.json'" % username)
            else:
                click.echo("File Created, name: '%s_posts.txt" % username)
            file.close()
        else:
            click.echo("Done!")
    except:
        click.echo(
            "Couldn't retrieve data, One of the following was the issue: \n1. Your query was wrong \n2. Instagram servers did not respond \n3. There is a problem with your internet connection")


@click.command()
@click.option('-query', prompt="Query", help="Search Term")
@click.option('-create-file', default="false", help="true: Create a file with the data | false: Will not create a file, false is default")
@click.option('--file-type', default="text", help="json: Create a json file | text: Create a text file, text is default")
def search(query, create_file, file_type):
    try:
        api_url = "https://www.instagram.com/web/search/topsearch/?query=$%s" % query
        req = requests.get(api_url)
        data = req.json()
        file = open("data.json", "w+")
        json.dump(data, file)
        file.close()
        click.echo("File Created, name: data.json")
    except:
        click.echo(
            "Couldn't retrieve data, One of the following was the issue: \n1. Your query was wrong \n2. Instagram servers did not respond \n3. There is a problem with your internet connection")


cli.add_command(getposts)
cli.add_command(getuser)
cli.add_command(getuserposts)
cli.add_command(search)

if __name__ == "__main__":
    cli()
