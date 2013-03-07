#!/bin/bash

# Make sure we’re using the latest Homebrew
brew update

# Upgrade any already-installed formulae
brew upgrade

# Install wget with IRI support
brew install wget --enable-iri

# Install everything else
brew install ack
brew install git
brew install hub
brew install tree
brew install mysql
brew install libmemcached
brew install nodejs

# Remove outdated versions from the cellar
brew cleanup