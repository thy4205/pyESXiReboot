from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect
import ssl

def restart_vm(vm_name, si):
    """
    Restart a VMware ESXi virtual machine using VMware Tools.

    :param vm_name: Name of the virtual machine
    :param si: Service instance object
    :return: None
    """
    # Get the virtual machine object
    vm = get_vm_by_name(si, vm_name)

    if not vm:
        print("Virtual machine '{}' not found".format(vm_name))
        return

    try:
        # Restart the virtual machine using VMware Tools
        vm.RebootGuest()
        print("Virtual machine '{}' restarted using VMware Tools".format(vm_name))
    except vmodl.MethodFault as error:
        print("Failed to restart virtual machine '{}': {}".format(vm_name, error))


def get_vm_by_name(si, vm_name):
    """
    Get a virtual machine object by its name.

    :param si: Service instance object
    :param vm_name: Name of the virtual machine
    :return: Virtual machine object or None
    """
    content = si.RetrieveContent()
    vm = None
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for c in container.view:
        if c.name == vm_name:
            vm = c
            break
    return vm

def wait_for_task(task):
    """
    Wait for a vSphere task to complete.

    :param task: Task object
    :return: None
    """
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            task_done = True
            break
        if task.info.state == vim.TaskInfo.State.error:
            raise task.info.error

def main():
    # vCenter or ESXi host details
    hostname = '192.168.1.18'
    username = 'username'
    password = 'password'
    vm_names = ['VMXP04']

    # Disable SSL certificate verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Connect to the vCenter or ESXi host
    si = SmartConnect(host=hostname, user=username, pwd=password, sslContext=context)

    for vm_name in vm_names:
        # Restart the virtual machine using VMware Tools
        restart_vm(vm_name, si)

    # Disconnect from the vCenter or ESXi host
    Disconnect(si)


if __name__ == '__main__':
    main()
