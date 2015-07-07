#
# src/isilon/lib/isi_newfs/newfs_v12.c:118
#
IFS_MAGIC_MAP = {
    'FS_MAGIC': '0x04f00d',
    'CG_MAGIC': '0x090255',
    'CGSUMM_MAGIC': '0x090274',
    'BH_MAGIC': '0xdeaff2fe',
    'BH_MAGIC_PRE_SB': '0xdeaff1ef',
    'MDS_MAGIC': '0xf9bc3f00',
    'MDS_MAGIC_MASK': '0xfffdff00',
    'MDS_MAGIC_NO_IDI': '0x00020000',
    'LIN_MASTER_MAGIC': '0xf9bc3f01',
    'LIN_MASTER_MAGIC_NO_IDI': '0xf9be3f01',
    'LIN_INNER_MAGIC_64': '0xf9be3f02',
    'LIN_LEAF_MAGIC_64': '0xf9be3f03',
    'IFM_INNER_MAGIC': '0xf9bc3f12',
    'IFM_LEAF_MAGIC': '0xf9bc3f13',
    'IFM_INNER_MAGIC_NO_IDI': '0xf9be3f12',
    'IFM_LEAF_MAGIC_NO_IDI': '0xf9be3f13',
    'DFM_INNER_MAGIC': '0xf9bc3f22',
    'DFM_LEAF_MAGIC': '0xf9bc3f23',
    'DFM_INNER_MAGIC_NO_IDI': '0xf9be3f22',
    'DFM_LEAF_MAGIC_NO_IDI': '0xf9be3f23',
    'IFM_ATTR_EXTBLK_MAGIC': '0xf9bc3f31',
    'IFM_ATTR_EXTBLK_MAGIC_NO_IDI': '0xf9be3f31',
    'LIN_INNER_MAGIC_NO_IDI': '0xf9be3f32',
    'LIN_LEAF_MAGIC_NO_IDI': '0xf9be3f33',
    'LIN_INNER_MAGIC': '0xf9bc3f32',
    'LIN_LEAF_MAGIC': '0xf9bc3f33',
    'STF_INNER_MAGIC': '0xf9bc3f41',
    'STF_LEAF_MAGIC': '0xf9bc3f42',
    'STF_INNER_MAGIC_NO_IDI': '0xf9be3f41',
    'STF_LEAF_MAGIC_NO_IDI': '0xf9be3f42',
    'STF_DELTA_BLOCK_MAGIC': '0xf9be3f43',
    'QDB_INNER_MAGIC': '0xf9bc3f51',
    'QDB_LEAF_MAGIC': '0xf9bc3f52',
    'QAB_MAGIC': '0xf9be3f53'
}

#
# Notes
#
# - use the form foo = <obj>(**kwargs)
#

class FsObj(object):
    def __init__(self):
        pass

    def make_node(self):
        pass

class Inode(object, FsObj):
    def __init__(self, baddr):
        CPR_CMD = "isi_cpr -r i"


class Lin(object, FsObj):
    def __init__(self, l):
        lin = self.l


#
# LinMaster: On-disk master block; root of LIN tree
# sys/ifs/lin/lin_on_disk.h: 10
#
# /** Represents an on-disk master block. */
# struct lin_master_od {
# 	/* 0x0000: MDS block magic number */
# 	uint32_t	magic;
#
# 	/* 0x0004: version and LIN tree info */
# 	uint32_t	version : 24;		/**< enum lin_master_version */
# 	uint32_t	lin_max_prot : 4;	/**< LIN tree max prot */
# 	uint32_t	lin_depth : 4;		/**< LIN tree depth */
#
# 	/* 0x0008: first un-allocated LIN */
# 	ifs_lin_t	next_lin;

# 	/* 0x0010: last used snapid */
# 	ifs_snapid_t	last_snapid;

# 	/* 0x0018: enum lin_collect_state */
# 	uint8_t		collect_state : 2;

# 	/* 0x0019: LIN tree root addresses */
# 	struct ifs_addr_od lin_root_addrs[MAX_MIRRORS];

# 	/* 0x0059: collect fields */
# 	struct ifs_collect_super_state 	collect_super_state;

# 	/* 0x006d: first un-alloced sin */
# 	ifs_sin_t	next_sin;

# 	/* 0x0075: serialized collect nosweep device lists */
# 	uint8_t		collect_nosweep[NOSWEEP_BUF_SIZE];

# 	/* 0x0275: first un-allocated PQ lin key (zero if unallocated) */
# 	ifs_lin_t			next_pq;

# 	/* 0x027D: unused space */
# 	uint8_t				padding[IFS_BSIZE - 8 -
# 					    NOSWEEP_BUF_SIZE - 117 - 9];
# 	/* 0x1ff7: IDI checksum */
# 	struct idi_dcode_9b idi;
# } __packed;
#

class LinMaster(object, FsObj):
    """foo
    """

    def __init__(self, **kwargs):
        super(LinMaster, self).__init__()
        self.magic = IFS_MAGIC_MAP['LIN_MASTER_MAGIC']
        self.version = kwargs['version']
        self.lin_max_prot = kwargs['maxprot']
        self.lin_depth = kwargs['depth']
        self.next_lin = kwargs['nextlin']
        self.last_snapid = kwargs['lastsnapid']
        self.collect_state = kwargs['collectstate']
        self.lin_root_addrs = kwargs['linroots']  # embedded dict?
        self.collect_super_state = kwargs['collectsuperstate']
        self.next_sin = kwargs['nextsin']
        self.collect_nosweep = kwargs['collectnosweep']
        self.next_pq = kwargs['nextpq']
        self.padding = None
        self.idi = kwargs['idi']

    @property
    def magic(self):
        return self.magic


# /**
#  * Superblock for an IFS file system.
#  */
# struct ifs_super {
# /* 0: */
# 	uint32_t  s_minor_version;	/**< version number for super format */
# 	uint32_t  s_magic;		/**< magic number */
# 	uint32_t  s_fmt_version;	/**< format version */
#
# 	/*
# 	 * The s_feature_bits field is used to prevent mounting incompatible
# 	 * file systems during a development cycle.  It should always be 0 on
# 	 * released OneFS versions.
# 	 */
# 	uint32_t  s_feature_bits;
#
# 	/*
# 	 * IDI:
# 	 */
# 	uint8_t   unused_idi_leader[3];
# 	struct idi_dcode_9b s_idi;	/**< The superblock checkcode */
# 	struct {} s_idi_second_part;
# 	/**<
# 	 * idi_second_part marks the start of second part of payload for
# 	 * idi checkcode.
# 	 */
#
# 	uint64_t  s_time;		/**< last time written */
# 	uint32_t  s_size;		/**< number of blocks on disk */
# 	ifs_devid_t s_devid;            /**< device id of the node */
# 	uint32_t  s_ncg;		/**< number of cylinder groups */
# 	struct block_history_super s_block_history_super;
# 	/**< block history status */
#
# /* 50: */
# /* this data must be re-computed after crashes */
# 	uint64_t  s_nifree;		/**< # of free inodes */
# 	uint32_t  s_nbfree;		/**< # of free blocks */
#
# /* 62: */
# /* these fields are cleared at mount time */
# 	uint8_t   s_purpose;            /**< drive purpose (Storage, L3, ...) */
# 	ifs_ldnum_t s_ldnum;		/**< drive ldnum */
# 	uint8_t   unused_at_64[1];
# 	uint8_t   s_flags;		/**< see FS_ flags below */
# 	ifs_guid  s_drive_guid;		/**< drive globally unique identifier */
#
# /* 82: */
# /* cluster specific fields */
# 	uint64_t  s_lin_master_baddrs_rev;
# 	/**< master_baddrs_rev for LIN-tree (requires drv_superblock_lock) */
# 	struct ifs_baddr s_lin_master_baddrs[MAX_MIRRORS];
# 	/**< master_baddrs for the LIN tree (requires drv_superblock_lock) */
#
# 	uint32_t  s_fmt_version_prev;	/**< previous stable fs fmt ver */
#
# 	uint8_t s_cluster_guid[IFSCONFIG_GUID_SIZE];
# 	/**< cluster globally unique identifier */
#
# 	struct ifs_collect_super s_collect_super_deprecated;
# 	/**< collect fields (and last snapid) are moved to lin_master and
# 	 * these values here are used until we are at stable Scotch Bonnet
# 	 * version.
# 	 */
#
# /* 204: */
# 	uint8_t   padding[820];
# }  __packed;
# CTASSERT(sizeof(struct ifs_super) == 1024);

class SuperBlock(object, FsObj):
    def __init__(self):
        pass
