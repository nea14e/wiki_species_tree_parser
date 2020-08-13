package github.nea14e.wiki_species_tree_parser.presenters.tree.view_entities;

import github.nea14e.wiki_species_tree_parser.entities.Level;

abstract public class BaseTreeViewLevel {
    public Level level;

    BaseTreeViewLevel(Level level) {
        this.level = level;
    }
}
