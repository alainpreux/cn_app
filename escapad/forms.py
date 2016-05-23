#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class RepositoryForm(forms.ModelForm):
    
    # FIXME : this validation occurs before username and name are populated in save() method user and name are always empty
    def clean(self):
        cleaned_data = super(RepositoryForm, self).clean()
        print("cleaned data = %s" % cleaned_data)
        user = cleaned_data.get("git_username")
        name = cleaned_data.get("git_name")

        # if not (user and name):
        #     raise forms.ValidationError(
        #         u'Les variables name and username doivent être unique ensemble, i.e il existe déjà un couple avec les valeurs git_user = %(user)s et git_name = %(name)s',
        #         code='unique_together_violated',
        #         params={'user':user, 'name':name}
        #         )
