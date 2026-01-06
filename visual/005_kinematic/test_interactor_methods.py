import pyvista as pv

p = pv.Plotter()
iren = p.iren

print("\n--- Available interactor methods ---")
for name in dir(iren):
    if "timer" in name.lower() or "observer" in name.lower():
        print(name)

print("\n--- Full list (optional) ---")
# print(dir(iren))