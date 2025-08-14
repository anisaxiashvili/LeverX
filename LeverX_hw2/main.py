import sys
from typing import List, Optional
from .cli.cli_controller import CLIController
from .exceptions.custom_exceptions import StudentRoomManagerError


def main(args: Optional[List[str]] = None) -> int:
    try:
        controller = CLIController()
        result = controller.run(args)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())