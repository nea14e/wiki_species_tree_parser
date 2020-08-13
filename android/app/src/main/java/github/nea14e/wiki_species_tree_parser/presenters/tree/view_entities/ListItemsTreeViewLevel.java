package github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities;

import java.util.List;

import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.entities.Level;

public class ListItemsTreeViewLevel extends BaseTreeViewLevel {
    public final List<Item> items;

    public ListItemsTreeViewLevel(Level level) {
        super(level);
        this.items = level.items;
    }
}
