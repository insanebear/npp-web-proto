import NavigationBar from './navigationBar'; 
import NavItem from './navItem';

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <NavigationBar>
        {/* Add the 'to' prop to each NavItem */}
        <NavItem text="Bayesian Methods" to="/bayesian" />
        <NavItem text="Statistical Methods" to="/statistical" />
      </NavigationBar>
      {children}
    </>
  );
};

export default Layout;