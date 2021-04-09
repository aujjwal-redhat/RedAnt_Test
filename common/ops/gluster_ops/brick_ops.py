"""
This part deals with the ops related to the bricks

class - BrickOps
"""

class BrickOps:
    """
    It provides the following functionalities:

    add_brick
    remove_brick
    replace_brick
    reset_brick
    """

    def add_brick(self, node: str, volname: str, bricks_list: list, force: bool = False, **kwargs):
        """
        This function adds bricks specified in the list (bricks_list)
        in the volume.

        Args:

            node(str): The node on which the command is to be run.
            volname(str): The volume in which the brick has to be added.
            bricks_list(list) : The list of bricks.

        Kwargs:
            
            force (bool): If this option is set to True, then add brick command
            will get executed with force option. If it is set to False,
            then add brick command will get executed without force option

            **kwargs
                The keys, values in kwargs are:
                    - replica_count : (int)|None
                    - arbiter_count : (int)|None
        """
        replica_count = arbiter_count = None

        if 'replica_count' in kwargs:
            replica_count = int(kwargs['replica_count'])

        if 'arbiter_count' in kwargs:
            arbiter_count = int(kwargs['arbiter_count'])
        
        replica = arbiter = ''

        if replica_count is not None:
            replica = f'replica {replica_count}'
        
            if arbiter_count is not None:
                arbiter = f'arbiter {arbiter_count}'
            
        force_value = ''

        if force:
            force_value = 'force'

        cmd = f"gluster volume add-brick {volname} {replica} {arbiter} {' '.join(bricks_list)} {force_value}"
        self.logger.info(f"Running {cmd} on {node}")
        ret = self.execute_command(node=node, cmd=cmd)

        if int(ret["error_code"]) != 0:
            self.logger.error(ret["error_msg"])
            raise Exception(ret["error_msg"])

        self.logger.info(f"Successfully ran {cmd} on {node}")
