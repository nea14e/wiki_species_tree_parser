package github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities;

import github.nea14e.wiki_species_tree_parser.entities.Item;
import github.nea14e.wiki_species_tree_parser.entities.Level;

public class ShortenedTreeViewLevel extends BaseTreeViewLevel {
    public final Level level;
    public final Item item;

    public ShortenedTreeViewLevel(Level level, Item item) {
        this.level = level;
        this.item = item;
    }
}
