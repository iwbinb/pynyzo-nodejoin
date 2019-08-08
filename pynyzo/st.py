from stem import CircStatus
from stem.control import Controller

with Controller.from_port(port = 10051) as controller:
  controller.authenticate()

  for circ in controller.get_circuits():
    if circ.status != CircStatus.BUILT:
      continue

    exit_fp, exit_nickname = circ.path[-1]

    exit_desc = controller.get_network_status(exit_fp, None)
    exit_address = exit_desc.address if exit_desc else 'unknown'

    print("Exit relay")
    print("fingerprint: {}").format(exit_fp)
    print("nickname: {}").format(exit_nickname)
    print("address: {}").format(exit_address)
