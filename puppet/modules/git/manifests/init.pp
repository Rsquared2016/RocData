class git {
    package {'git':
      name   => "git",
      ensure => latest,
    }
}