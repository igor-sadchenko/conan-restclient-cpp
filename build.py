from conan.packager import ConanMultiPackager
import os, re


def get_value_from_recipe(search_string):
    with open("conanfile.py", "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result

def get_name_from_recipe():
    return get_value_from_recipe(r'''name\s*=\s*["'](\S*)["']''').groups()[0]

def get_version_from_recipe():
    return get_value_from_recipe(r'''version\s*=\s*["'](\S*)["']''').groups()[0]


if __name__ == "__main__":
    header_only = False
    name = get_name_from_recipe()
    version = get_version_from_recipe()
    reference = "{0}/{1}@".format(name, version)
    username = "conan"
    upload_remote = "https://api.bintray.com/conan/{0}/conan/".format(username)

    builder = ConanMultiPackager(
        login_username=username,
        reference=reference,
        upload=upload_remote,
        remotes=upload_remote,
        build_policy="missing",
        visual_toolsets=['v140', 'v141', 'v142'],
        apple_clang_versions=['11.0'],
        password="conanbot",
        upload_dependencies="all"
    )

    if header_only:
        filtered_builds = []
        for settings, options, env_vars, build_requires, reference in builder.items:
            if settings["compiler"] == "gcc":
                filtered_builds.append([settings, options, env_vars, build_requires])
                break
        builder.builds = filtered_builds

    builder.add_common_builds()
    builder.run()
