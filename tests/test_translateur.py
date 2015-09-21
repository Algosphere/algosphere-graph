"""
Test Translateur class
"""

import pytest
import sys

sys.path.append('src')

from translateur import Translateur

def get_translateur():
    translations = {'ci 1':'ci one', 'ci 2':'ci two', 'ci 3':'ci three'}
    translateur = Translateur('english', 'en', translations)
    return translateur

def test_translate():
    """ Test the translate method """
    translate = get_translateur().translate
    assert translate('ci 1') == 'ci one'
    assert translate('ci 2') == 'ci two'
    assert translate('ci 3') == 'ci three'
    assert translate('no ci') == None

def test_add_translation():
    """ Test the add_translation method """
    translateur = get_translateur()
    translateur.add_translation('ci 4', 'ci four')
    assert translateur.translate('ci 4') == 'ci four'

def test_add_existing_translation():
    """ Test the add_translation method with a already existing translation """
    translateur = get_translateur()
    with pytest.raises(ValueError):
        translateur.add_translation("ci 3", "ci three again")
