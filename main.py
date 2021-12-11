from googleplay import GooglePlay

categories = ["social"]
gp = GooglePlay("https://apkcombo.com")
apps = gp.get_app_list(categories)
gp.save_apps_list(apps)
gp.download_apps_apk(apps)