"""
    Module Name:
    Purpose: Refer to the redhat_mixin.md for more information
"""
from common.rexe import Rexe
from common.relog import Logger
from common.ops.support_ops.io_ops import IoOps
from common.ops.gluster_ops.peer_ops import PeerOps
from common.ops.gluster_ops.volume_ops import VolumeOps
from common.ops.gluster_ops.gluster_ops import GlusterOps


class RedantMixin(GlusterOps, VolumeOps, PeerOps, IoOps, Rexe, Logger):
    """
    A mixin class for redant project to encompass all ops and support
    modules.
    """
    pass
