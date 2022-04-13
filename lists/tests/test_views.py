from django.test import TestCase
from django.urls import reverse
from lists.models import Item, List


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(reverse("view_list", args=[list_.id]))
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(reverse("view_list", args=[correct_list.id]))
        self.assertEqual(response.context["list"], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=other_list)
        Item.objects.create(text="other list item 2", list=other_list)

        response = self.client.get(reverse("view_list", args=[correct_list.id]))

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")
