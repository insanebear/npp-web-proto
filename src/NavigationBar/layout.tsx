import NavigationBar from './navigationBar'; 
import NavItem from './navItem';

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <NavigationBar>
        {/* Add the 'to' prop to each NavItem */}
        <NavItem text="Bayesian Methods" to="/" position={{ x: '10%', y: '50%' }} />
        <NavItem text="Statistical Methods" to="/statistical" position={{ x: '24%', y: '50%' }} />
        <NavItem text="Reliability Views" to="/reliability-views" position={{ x: '39.5%', y: '50%' }} />
        <NavItem text="Settings" to="/settings" position={{ x: '95%', y: '50%' }} />
      </NavigationBar>
      {children}
    </>
  );
};

export default Layout;