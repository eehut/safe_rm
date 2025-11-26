
.PHONY: install uninstall

install:
	@echo "Installing srm to /usr/bin..."
	sudo cp rm.py /usr/bin/rm.py
	sudo chmod +x /usr/bin/rm.py
	sudo ln -sf /usr/bin/rm.py /usr/bin/srm
	@echo "Installation complete. You can now use 'srm' command."

uninstall:
	@echo "Uninstalling srm..."
	sudo rm -f /usr/bin/rm.py /usr/bin/srm
	@echo "Uninstallation complete."

# Default target
all: install

