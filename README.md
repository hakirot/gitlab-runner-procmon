# Gitlab-Runner Process Monitor

Errantly stalled Packer processes are commonly orphaned after the job shell is
terminated by GitLab, creating zombie packer processes that consume resources
and eventually prevent the allocation of more virtual machines. This script is
meant to be configured as the pre_build_script for runners that are configured
as the shell executor for packer builds in a pipeline. It reliably seeks one
packer instance per job, and sends the proper kill signal to the packer process
when the gitlab shell environment variable CI_JOB_TIMEOUT length is exceeded,
or the job is manually cancelled via the GitLab web UI.

    /etc/gitlab-runner/config.toml
        [[runners]]
            ...
            pre_build_script = "/usr/bin/gitlab-runner-procmon"
            ...

## BUILD
From project root, build rpm via

`rpmbuild -bb ./rpmbuild/SPECS/gitlab-runner-procmon.spec --define="_topdir $(pwd)/rpmbuild"`

## LOCAL INSTALLATION
`yum install rpmbuild/RPMS/[rpm]`
