#!/usr/bin/env python

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The American Gut Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "unversioned"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki.vazquezbaeza@colorado.edu"

from re import compile, findall, escape

def format_print_for_magnified_sample(sample_id, per_sample_file_string,
        global_file_string, preserve_Z_position=False):
    """Format SVG files as generated by Emperor for per sample figures

    Inputs:
    sample_id: identifier to look for in both files
    per_sample_file_string: file containing a single sample highlighted
    global_file_string: file containing multiple elements where the single
    sample is highlighted
    preserve_Z_position: whether the highlighted object should or should not be
    positioned in the correct place depth-wise

    Output:
    formatted_string: SVG formatted string where the sample_id element is
    highlighed in the global_file_string

    Raises:
    RuntimeError, if there's an inconsistency or there are non-matching sample
    identifiers between files
    """

    escaped_sample_id = escape(sample_id)

    re = compile('\\<path\ id\=\"'+escaped_sample_id+'\"\ d\=\\"M\\ ([A-Za-z0-9\\.\\ \\-\\,]+)\\" style\\=\\"([A-Za-z0-9\\.\\ \\-\\,\\(\\)\\:\\;]+)\\"\\>\\<\\/path\\>')

    big_sphere_contents = findall(re, per_sample_file_string)
    small_sphere_contents = findall(re, global_file_string)

    # this indicates an internal inconsistency so let the user know
    if big_sphere_contents == [] or small_sphere_contents == []:
        raise RuntimeError, "There's a problem with the formatting of the SVG"+\
            " files"

    temp = global_file_string

    matchable = '<path id="%s"' % sample_id
    matchable = matchable + ' d="M %s" style="%s"></path>'

    # this will make the sample to be placed in it's correct Z position
    if preserve_Z_position:
        # iter over each of the matches
        for index in range(0, min([len(small_sphere_contents),
            len(big_sphere_contents)])):
            temp = temp.replace(matchable % small_sphere_contents[index],
                matchable % big_sphere_contents[index])
    # this will make the sample positioned at the very top of the plot
    else:
        # remove all the occurrences of such object from the plot
        for index in range(0, len(small_sphere_contents)):
            temp = temp.replace(matchable % small_sphere_contents[index], '')
        # append at the very end the object to the plot
        temp = temp.replace('</svg>', ''.join([matchable % element for element
            in big_sphere_contents])+'</svg>')

    return temp
