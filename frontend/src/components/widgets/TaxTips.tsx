import { Lightbulb, TrendingUp, Shield, Users } from 'lucide-react';

export default function TaxTips() {
  const tips = [
    {
      id: 1,
      title: "Maximize Section 80C",
      description: "Invest in ELSS, PPF, or life insurance to save up to ₹46,800 in taxes annually (at 30% tax bracket).",
      icon: TrendingUp,
      color: "blue"
    },
    {
      id: 2,
      title: "Health Insurance Benefits",
      description: "Claim deductions for health insurance premiums under Section 80D - up to ₹25,000 for self and family, plus additional for senior citizen parents.",
      icon: Shield,
      color: "green"
    },
    {
      id: 3,
      title: "Home Loan Advantages",
      description: "Claim both principal repayment under Section 80C and interest payment under Section 24(b) for home loans.",
      icon: Users,
      color: "purple"
    },
    {
      id: 4,
      title: "Donate and Save",
      description: "Donations to approved charitable institutions under Section 80G can give you 50% or 100% tax benefit.",
      icon: Lightbulb,
      color: "yellow"
    }
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
        <Lightbulb className="h-5 w-5 text-blue-600" />
        Tax Saving Tips
      </h2>

      <div className="space-y-4">
        {tips.map((tip) => (
          <div key={tip.id} className="p-4 border-l-4 border-[var(--tip-color)] bg-[var(--tip-bg)]">
            <div className="flex items-start space-x-3">
              <div className={`w-8 h-8 flex items-center justify-center rounded-full bg-${tip.color}-50 flex-shrink-0`}>
                <tip.icon className={`h-4 w-4 text-${tip.color}-600`} />
              </div>
              <div className="flex-1 space-y-1">
                <h3 className="text-sm font-medium text-gray-900">{tip.title}</h3>
                <p className="text-sm text-gray-600">{tip.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-3 border-t border-gray-100 text-sm text-gray-500 text-center">
        More tips available in the Chat Advisor section
      </div>
    </div>
  );
}